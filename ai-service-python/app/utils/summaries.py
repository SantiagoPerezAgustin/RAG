from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import OLLAMA_BASE_URL, OLLAMA_LLM_MODEL


def make_summary(user_message: str, assistant_message: str, max_sentences: int = 3) -> str:
    llm = ChatOllama(model=OLLAMA_LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
    prompt = (
        f"Resume en {max_sentences} frases cortas (español) el tema de la consulta y la solución dada. "
        "Solo texto, sin título."
    )
    out = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=f"Usuario: {user_message}\nAsistente: {assistant_message}"),
    ])
    return out.content.strip() if hasattr(out, "content") else str(out).strip()