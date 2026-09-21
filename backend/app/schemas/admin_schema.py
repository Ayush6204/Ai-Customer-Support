from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AdminUserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminDocumentResponse(BaseModel):
    id: int
    user_id: int
    session_id: int | None = None
    filename: str
    file_path: str
    file_type: str
    chroma_collection: str
    status: str
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminLogResponse(BaseModel):
    message: str
    data: dict[str, Any] | None = None