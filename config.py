import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Explicitly load .env from project root
load_dotenv(BASE_DIR / ".env")

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
STORAGE_DIR = BASE_DIR / "storage" / "faiss_index"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "4"))

DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Debug output
print("GROQ_API_KEY Loaded:", "YES" if GROQ_API_KEY else "NO")
print("Using model:", GROQ_MODEL)