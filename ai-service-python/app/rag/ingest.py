from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import KNOWLEDGE_DIR
from app.rag.retriever import get_embeddings, get_vector_store

def ingest_documents(source_path: str | None = None):
    base = Path(KNOWLEDGE_DIR)
    if source_path:
        base = base / source_path
    if not base.exists():
        return 0
    docs = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(path)).load())
        elif path.suffix.lower() in (".txt", ".md"):
            docs.extend(TextLoader(str(path)).load())
    if not docs:
        return 0
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    splits = splitter.split_documents(docs)
    vector_store = get_vector_store()
    vector_store.add_documents(splits)
    return len(splits)