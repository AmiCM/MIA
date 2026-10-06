from google import genai
from google.genai import types

from . import config

_client = None
BATCH = 50


def _get_client() -> genai.Client:
    global _client
    if not config.GOOGLE_API_KEY:
        raise RuntimeError("Falta GOOGLE_API_KEY en el entorno / .env")
    if _client is None:
        _client = genai.Client(api_key=config.GOOGLE_API_KEY)
    return _client


def _embed(texts: list[str], task_type: str) -> list[list[float]]:
    client = _get_client()
    out: list[list[float]] = []
    for i in range(0, len(texts), BATCH):
        res = client.models.embed_content(
            model=config.EMBED_MODEL,
            contents=texts[i:i + BATCH],
            config=types.EmbedContentConfig(task_type=task_type),
        )
        out.extend(e.values for e in res.embeddings)
    return out


def embed_documents(texts: list[str]) -> list[list[float]]:
    return _embed(texts, "RETRIEVAL_DOCUMENT")


def embed_query(text: str) -> list[float]:
    return _embed([text], "RETRIEVAL_QUERY")[0]
