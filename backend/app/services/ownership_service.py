from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession
from app.models.document import Document


def validate_session_owner(
    db: Session,
    session_id: int,
    current_user_id: int
):
    # print("ownership service (validate session) -->")
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    if session.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this session"
        )
    print(session)

    return session


def validate_document_owner(
    db: Session,
    document_id: int,
    current_user_id: int
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if document.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this document"
        )

    return document


def validate_document_session_owner(
    db: Session,
    document_id: int,
    session_id: int,
    current_user_id: int
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if document.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this document"
        )

    if document.session_id != session_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This document does not belong to this chat session"
        )

    return document