import chromadb

from . import config

_client = chromadb.PersistentClient(path=config.CHROMA_DIR)
# Espacio coseno: score = 1 - distancia. Los vectores los pasamos nosotros (Google AI).
_col = _client.get_or_create_collection(config.COLLECTION, metadata={"hnsw:space": "cosine"})


def count() -> int:
    return _col.count()


def delete_source(source: str) -> None:
    _col.delete(where={"source": source})


def list_sources() -> list[dict]:
    metas = _col.get(include=["metadatas"])["metadatas"]
    counts: dict[str, int] = {}
    for m in metas:
        counts[m["source"]] = counts.get(m["source"], 0) + 1
    return [{"source": k, "chunks": v} for k, v in sorted(counts.items())]


def add_chunks(source: str, chunks: list[str], vectors: list[list[float]]) -> int:
    delete_source(source)  # reingestar el mismo archivo no duplica
    _col.add(
        ids=[f"{source}::{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=vectors,
        metadatas=[{"source": source, "chunk_index": i} for i in range(len(chunks))],
    )
    return len(chunks)


def query(vector: list[float], top_k: int, source: str | None = None) -> list[dict]:
    if _col.count() == 0:
        return []
    res = _col.query(
        query_embeddings=[vector],
        n_results=top_k,
        where={"source": source} if source else None,
    )
    return [
        {"id": id_, "source": meta["source"], "chunk_index": meta["chunk_index"],
         "text": doc, "score": round(1 - dist, 4)}
        for id_, doc, meta, dist in zip(
            res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
        )
    ]
