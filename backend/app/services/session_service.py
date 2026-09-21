from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.chat_repository import (
    create_chat_session,
    get_user_chat_sessions,
    get_user_chat_session_by_id,
    update_chat_session_title,
    delete_chat_session,
    get_user_chat_messages,
)


def generate_default_session_title(db: Session, user_id: int) -> str:
    """
    Auto-generate title based on user's session count.
    Example:
    New Chat 1
    New Chat 2
    """

    existing_sessions = get_user_chat_sessions(
        db=db,
        user_id=user_id
    )

    next_number = len(existing_sessions) + 1

    return f"New Chat {next_number}"


def create_session_service(
    db: Session,
    current_user,
    title: str | None = None
):
    if not title or not title.strip():
        title = generate_default_session_title(
            db=db,
            user_id=current_user.id
        )

    session = create_chat_session(
        db=db,
        user_id=current_user.id,
        title=title.strip()
    )

    return {
        "session_id": session.id,
        "title": session.title,
        "message": "Chat session created successfully"
    }


def get_my_sessions_service(
    db: Session,
    current_user
):
    return get_user_chat_sessions(
        db=db,
        user_id=current_user.id
    )


def get_session_details_service(
    db: Session,
    current_user,
    session_id: int
):
    session = get_user_chat_session_by_id(
        db=db,
        user_id=current_user.id,
        session_id=session_id
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    messages = get_user_chat_messages(
        db=db,
        user_id=current_user.id,
        session_id=session.id
    )

    return {
        "id": session.id,
        "user_id": session.user_id,
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "messages": messages
    }


def rename_session_service(
    db: Session,
    current_user,
    session_id: int,
    title: str
):
    session = update_chat_session_title(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
        title=title.strip()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    return session


def delete_session_service(
    db: Session,
    current_user,
    session_id: int
):
    session = delete_chat_session(
        db=db,
        user_id=current_user.id,
        session_id=session_id
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    return {
        "message": "Chat session deleted successfully"
    }