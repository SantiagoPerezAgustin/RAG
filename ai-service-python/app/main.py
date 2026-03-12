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

        history_text = ""
        if req.history:
            for m in req.history[-10:]:
                role = (m.get("role") or m.get("Role") or "").strip()
                content = (m.get("content") or m.get("Content") or "").strip()
                if not content:
                    continue
                if role.lower() in ("user", "human"):
                    history_text += f"Usuario: {content}\n"
                elif role.lower() in ("assistant", "bot", "ai"):
                    history_text += f"Asistente: {content}\n"
                else:
                    history_text += f"{role or 'Usuario'}: {content}\n"

        if history_text:
            full_question = f"{history_text}\nUsuario: {req.message}"
        else:
            full_question = req.message

        answer = chain.invoke(full_question)
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