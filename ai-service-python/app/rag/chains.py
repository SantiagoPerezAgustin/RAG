from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.config import OLLAMA_BASE_URL, OLLAMA_LLM_MODEL
from app.rag.retriever import get_retriever

SYSTEM_PROMPT = """Eres un asistente de soporte técnico nivel 1. Responde en español de forma clara y breve.
Si la información del contexto no es suficiente, di que no tienes esa información y sugiere contactar a soporte nivel 2.
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