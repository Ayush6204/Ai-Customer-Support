from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CreateSessionRequest(BaseModel):
    title: str | None = None


class UpdateSessionRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class SessionResponse(BaseModel):
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionCreateResponse(BaseModel):
    session_id: int
    title: str
    message: str


class DeleteSessionResponse(BaseModel):
    message: str