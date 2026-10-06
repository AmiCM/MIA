import io
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader

from . import config, embed, generate, store
from .chunk import chunk_text

app = FastAPI(title="RAG API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


class QueryIn(BaseModel):
    question: str
    top_k: int = config.TOP_K
    source: str | None = None  # reto opcional: filtrar por archivo
    retrieve_only: bool = False  # solo recuperar (sin Gemini); útil para calibrar MIN_SCORE


def _extract(name: str, data: bytes) -> str:
    if name.lower().endswith(".pdf"):
        return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    return data.decode("utf-8", errors="ignore")


@app.get("/health")
def health():
    return {"status": "ok", "chroma_chunks": store.count(),
            "api_key_set": bool(config.GOOGLE_API_KEY)}


@app.get("/sources")
def sources():
    return {"sources": store.list_sources()}


@app.delete("/sources/{source}")
def delete_source(source: str):
    if source not in {s["source"] for s in store.list_sources()}:
        raise HTTPException(404, f"No existe la fuente {source}")
    store.delete_source(source)
    return {"deleted": source, "index_size": store.count()}


@app.post("/ingest")
async def ingest(files: list[UploadFile] = File(...)):
    if not config.GOOGLE_API_KEY:
        raise HTTPException(503, "GOOGLE_API_KEY no configurada")
    docs = total = 0
    skipped = []
    for f in files:
        text = _extract(f.filename, await f.read())
        chunks = chunk_text(text, config.CHUNK_WORDS, config.CHUNK_OVERLAP)
        if not chunks:
            skipped.append(f.filename)  # vacío / PDF escaneado
            continue
        try:
            vectors = embed.embed_documents(chunks)
        except Exception as e:
            raise HTTPException(502, f"Error de Google AI al incrustar {f.filename}: {e}")
        total += store.add_chunks(Path(f.filename).name, chunks, vectors)
        docs += 1
    return {"documents": docs, "chunks": total, "skipped": skipped,
            "index_size": store.count()}


@app.post("/query")
def query(body: QueryIn):
    question = body.question.strip()
    if not question:
        raise HTTPException(422, "La pregunta está vacía")
    if not config.GOOGLE_API_KEY:
        raise HTTPException(503, "GOOGLE_API_KEY no configurada")
    try:
        hits = store.query(embed.embed_query(question), body.top_k, body.source)
        if body.retrieve_only:
            return {"answer": "", "citations": hits, "abstained": False}
        if not hits or hits[0]["score"] < config.MIN_SCORE:
            return {"answer": generate.ABSTAIN_MSG, "citations": hits, "abstained": True}
        text, abstained = generate.answer(question, hits)
    except Exception as e:
        raise HTTPException(502, f"Error de Google AI: {e}")
    return {"answer": text, "citations": hits, "abstained": abstained}
