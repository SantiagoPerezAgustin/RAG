from fastapi import FastAPI, HTTPException
from app.models import ChatRequest, ChatResponse, IngestRequest
from app.rag.chains import build_rag_chain
from app.rag.ingest import ingest_documents
from app.utils.summaries import make_summary

app = FastAPI(title="Soporte Técnico RAG API (Ollama)")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        chain = build_rag_chain()
        answer = chain.invoke(req.message)
        summary = make_summary(req.message, answer)
        return ChatResponse(answer=answer, summary=summary, sources=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest")
def ingest(req: IngestRequest | None = None):
    try:
        n = ingest_documents(req.source_path if req else None)
        return {"ingested": n, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))