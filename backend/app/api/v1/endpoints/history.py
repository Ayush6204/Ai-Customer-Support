from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import require_user
from app.schemas.history_schema import (
    ChatMessageResponse,
    DeleteMessageResponse,
)
from app.services.history_service import (
    get_my_history_service,
    delete_message_service,
)


router = APIRouter(prefix="/history", tags=["History"])


@router.get(
    "",
    response_model=list[ChatMessageResponse]
)
def get_my_history(
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    return get_my_history_service(
        db=db,
        current_user=current_user
    )


@router.delete(
    "/{message_id}",
    response_model=DeleteMessageResponse
)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    return delete_message_service(
        db=db,
        current_user=current_user,
        message_id=message_id
    )