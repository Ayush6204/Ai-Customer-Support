from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import require_user
from app.schemas.chat_schema import (
    AskQuestionRequest,
    AskQuestionResponse,
)
from app.services.chat_service import ask_question_service



router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/ask",
    response_model=AskQuestionResponse
)
def ask_question(
    request: AskQuestionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    # print("chat endpoint-->")
    return ask_question_service(
        db=db,
        current_user=current_user,
        session_id=request.session_id,
        question=request.question,
        document_id=request.document_id,
    )