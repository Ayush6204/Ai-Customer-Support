from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class SourceReference(BaseModel):
    document_id: str | int | None = None
    filename: str | None = None
    chunk_index: int | str | None = None
    similarity_score: float | None = None
    preview: str | None = None


class ChatMessageResponse(BaseModel):
    id: int
    user_id: int
    session_id: int
    document_id: int | None = None
    question: str
    answer: str
    sources: list[SourceReference] | list[dict[str, Any]] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeleteMessageResponse(BaseModel):
    message: str