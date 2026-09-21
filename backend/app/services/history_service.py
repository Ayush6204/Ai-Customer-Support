from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.chat_repository import (
    get_user_all_chat_messages,
    get_user_chat_messages,
    delete_user_chat_message,
)
from app.services.ownership_service import validate_session_owner


def get_my_history_service(
    db: Session,
    current_user
):
    """
    Return all history for current user only.
    """

    return get_user_all_chat_messages(
        db=db,
        user_id=current_user.id
    )


def get_session_messages_service(
    db: Session,
    current_user,
    session_id: int
):
    """
    Validate session ownership, then return messages.
    """

    session = validate_session_owner(
        db=db,
        session_id=session_id,
        current_user_id=current_user.id
    )

    return get_user_chat_messages(
        db=db,
        user_id=current_user.id,
        session_id=session.id
    )


def delete_message_service(
    db: Session,
    current_user,
    message_id: int
):
    """
    Delete message only if it belongs to current user.
    """

    deleted_message = delete_user_chat_message(
        db=db,
        user_id=current_user.id,
        message_id=message_id
    )

    if not deleted_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    return {
        "message": "Chat message deleted successfully"
    }