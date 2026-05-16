from pathlib import Path

from langchain_community.vectorstores import FAISS

from config import DOCUMENTS_DIR, STORAGE_DIR
from rag.document_loader import load_directory, load_documents
from rag.embeddings import get_embeddings
from rag.qa_chain import build_qa_chain
from rag.text_splitter import split_documents
from rag.vector_store import (
    build_vector_store,
    get_retriever,
    load_vector_store,
    save_vector_store,
)


class KnowledgeCopilot:
    """End-to-end RAG: Documents → Loader → Splitter → Embeddings → FAISS → Groq QA."""

    def __init__(self):
        self.embeddings = get_embeddings()
        self.vector_store: FAISS | None = load_vector_store(self.embeddings)
        self._qa_invoke = None

    @property
    def is_ready(self) -> bool:
        return self.vector_store is not None

    def ingest_paths(self, paths: list[Path]) -> int:
        documents = load_documents(paths)
        return self._ingest_documents(documents)

    def ingest_directory(self, directory: Path | None = None) -> int:
        documents = load_directory(directory or DOCUMENTS_DIR)
        return self._ingest_documents(documents)

    def _ingest_documents(self, documents) -> int:
        if not documents:
            return 0

        chunks = split_documents(documents)
        new_store = build_vector_store(chunks, self.embeddings)

        if self.vector_store:
            self.vector_store.merge_from(new_store)
        else:
            self.vector_store = new_store

        save_vector_store(self.vector_store, STORAGE_DIR)
        self._qa_invoke = None
        return len(chunks)

    def ask(self, question: str) -> dict:
        if not self.is_ready:
            raise RuntimeError(
                "Knowledge base is empty. Upload documents and build the index first."
            )
        if self._qa_invoke is None:
            self._qa_invoke = build_qa_chain(get_retriever(self.vector_store))
        return self._qa_invoke(question)

    def reset_index(self) -> None:
        self.vector_store = None
        self._qa_invoke = None
        for pattern in ("*.faiss", "*.pkl"):
            for file in STORAGE_DIR.glob(pattern):
                file.unlink(missing_ok=True)
