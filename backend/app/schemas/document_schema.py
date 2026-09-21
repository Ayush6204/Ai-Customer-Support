from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    # print("document schema -->")
    id: int
    user_id: int
    session_id: int
    filename: str
    file_path: str
    file_type: str
    chroma_collection: str
    status: str
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)