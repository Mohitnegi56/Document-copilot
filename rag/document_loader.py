from pathlib import Path

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}


def load_documents(paths: list[Path]) -> list[Document]:
    documents: list[Document] = []
    for path in paths:
        suffix = path.suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            continue
        loader = _get_loader(path, suffix)
        loaded = loader.load()
        for doc in loaded:
            doc.metadata["source"] = str(path.name)
        documents.extend(loaded)
    return documents


def load_directory(directory: Path) -> list[Document]:
    paths = [
        p
        for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return load_documents(paths)


def _get_loader(path: Path, suffix: str):
    if suffix == ".pdf":
        return PyPDFLoader(str(path))
    if suffix == ".docx":
        return Docx2txtLoader(str(path))
    return TextLoader(str(path), encoding="utf-8")
