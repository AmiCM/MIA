import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
EMBED_MODEL = os.getenv("EMBED_MODEL", "gemini-embedding-001")
GEN_MODEL = os.getenv("GEN_MODEL", "gemini-3.8-flash")
CHROMA_DIR = os.getenv("CHROMA_DIR", str(BASE_DIR / "chroma"))
COLLECTION = "rag_docs"

CHUNK_WORDS = int(os.getenv("CHUNK_WORDS", 250))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
TOP_K = int(os.getenv("TOP_K", 4))
# Similitud coseno mínima del mejor chunk; por debajo, se abstiene sin llamar a Gemini.
MIN_SCORE = float(os.getenv("MIN_SCORE", 0.63))
