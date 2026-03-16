from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.config import OLLAMA_BASE_URL, OLLAMA_LLM_MODEL
from app.rag.retriever import get_retriever

SYSTEM_PROMPT = """Eres un asistente de soporte técnico. Responde siempre en español de forma clara y breve.

Usa el contexto de documentación técnica que se muestra abajo cuando sea relevante para la pregunta del usuario.
Si el contexto no contiene exactamente la respuesta, igual intenta dar una respuesta útil basándote en tu conocimiento general y en buenas prácticas de soporte.

No digas que no tienes información salvo que realmente no puedas ayudar. Solo en esos casos podés sugerir que la persona contacte a soporte humano, pero sin mencionar niveles de soporte (nivel 1, nivel 2, etc.).

Contexto (documentación técnica):
{context}
"""

def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

def build_rag_chain():
    llm = ChatOllama(
        model=OLLAMA_LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.3,
    )
    retriever = get_retriever(k=4)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain