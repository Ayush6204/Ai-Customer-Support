from datetime import datetime
from pydantic import BaseModel, Field


class AskQuestionRequest(BaseModel):
    # print("chat schema (request model)-->")
    session_id: int
    question: str = Field(..., min_length=1)
    document_id: int | None = None


class SourceResponse(BaseModel):
    document_id: str | int | None = None
    filename: str | None = None
    chunk_index: int | str | None = None
    similarity_score: float | None = None
    preview: str | None = None


class AskQuestionResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    contexts: list[str]
    session_id: int
    timestamp: datetime