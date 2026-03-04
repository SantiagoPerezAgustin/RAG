from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    message: str
    channel: Optional[str] = None
    history: Optional[list[dict]] = None

class SourceDoc(BaseModel):
    content: str
    metadata: Optional[dict] = None

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[list[SourceDoc]] = None
    summary: Optional[str] = None

class IngestRequest(BaseModel):
    source_path: Optional[str] = None