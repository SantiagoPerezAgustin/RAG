from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from app.config import CHROMA_PERSIST_DIR, COLLECTION_NAME, OLLAMA_BASE_URL, OLLAMA_EMBEDDING_MODEL

def get_embeddings():
    return OllamaEmbeddings(
        model=OLLAMA_EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

def get_vector_store():
    embeddings = get_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

def get_retriever(k: int = 4):
    vector_store = get_vector_store()
    return vector_store.as_retriever(search_kwargs={"k": k})