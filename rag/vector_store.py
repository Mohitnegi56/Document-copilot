from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from config import RETRIEVAL_K, STORAGE_DIR


INDEX_NAME = "enterprise_kb"


def build_vector_store(
    chunks: list[Document], embeddings: Embeddings
) -> FAISS:
    return FAISS.from_documents(chunks, embeddings)


def save_vector_store(store: FAISS, directory: Path | None = None) -> Path:
    target = directory or STORAGE_DIR
    store.save_local(str(target), index_name=INDEX_NAME)
    return target


def load_vector_store(
    embeddings: Embeddings, directory: Path | None = None
) -> FAISS | None:
    target = directory or STORAGE_DIR
    index_path = target / f"{INDEX_NAME}.faiss"
    if not index_path.exists():
        return None
    return FAISS.load_local(
        str(target),
        embeddings,
        index_name=INDEX_NAME,
        allow_dangerous_deserialization=True,
    )


def get_retriever(store: FAISS, k: int | None = None):
    return store.as_retriever(search_kwargs={"k": k or RETRIEVAL_K})
