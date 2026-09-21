from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import require_user
from app.schemas.session_schema import (
    CreateSessionRequest,
    UpdateSessionRequest,
    SessionResponse,
    SessionCreateResponse,
    DeleteSessionResponse,
)
from app.services.session_service import (
    create_session_service,
    get_my_sessions_service,
    get_session_details_service,
    rename_session_service,
    delete_session_service,
)
from app.schemas.history_schema import ChatMessageResponse
from app.services.history_service import get_session_messages_service


router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post(
    "",
    response_model=SessionCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def create_session(
    request: CreateSessionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    return create_session_service(
        db=db,
        current_user=current_user,
        title=request.title
    )


@router.get(
    "",
    response_model=list[SessionResponse]
)
def get_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    return get_my_sessions_service(
        db=db,
        current_user=current_user
    )


@router.get("/{session_id}")
def get_session_details(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    return get_session_details_service(
        db=db,
        current_user=current_user,
        session_id=session_id
    )


@router.patch(
    "/{session_id}",
    response_model=SessionResponse
)
def rename_session(
    session_id: int,
    request: UpdateSessionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    return rename_session_service(
        db=db,
        current_user=current_user,
        session_id=session_id,
        title=request.title
    )


@router.delete(
    "/{session_id}",
    response_model=DeleteSessionResponse
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    return delete_session_service(
        db=db,
        current_user=current_user,
        session_id=session_id
    )
    
@router.get(
    "/{session_id}/messages",
    response_model=list[ChatMessageResponse]
)
def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    return get_session_messages_service(
        db=db,
        current_user=current_user,
        session_id=session_id
    )