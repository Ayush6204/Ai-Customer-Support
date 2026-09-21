from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage


def create_chat_session(
    db: Session,
    user_id: int,
    title: str = "New Chat"
):
    session = ChatSession(
        user_id=user_id,
        title=title
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_user_chat_sessions(
    db: Session,
    user_id: int
):
    return db.query(ChatSession).filter(
        ChatSession.user_id == user_id
    ).order_by(
        desc(ChatSession.created_at)
    ).all()


def get_user_chat_session_by_id(
    db: Session,
    user_id: int,
    session_id: int
):
    return db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()


def update_chat_session_title(
    db: Session,
    user_id: int,
    session_id: int,
    title: str
):
    session = get_user_chat_session_by_id(
        db=db,
        user_id=user_id,
        session_id=session_id
    )

    if not session:
        return None

    session.title = title

    db.commit()
    db.refresh(session)

    return session


def delete_chat_session(
    db: Session,
    user_id: int,
    session_id: int
):
    session = get_user_chat_session_by_id(
        db=db,
        user_id=user_id,
        session_id=session_id
    )

    if not session:
        return None

    db.delete(session)
    db.commit()

    return session


def create_chat_message(
    db: Session,
    user_id: int,
    session_id: int,
    document_id: int | None,
    question: str,
    answer: str,
    sources: list | None = None,
):
    print("chat repository (create message) -->")
    message = ChatMessage(
        user_id=user_id,
        session_id=session_id,
        document_id=document_id,
        question=question,
        answer=answer,
        sources=sources,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_user_chat_messages(
    db: Session,
    user_id: int,
    session_id: int
):
    return db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id,
        ChatMessage.session_id == session_id
    ).order_by(
        ChatMessage.created_at
    ).all()


def get_recent_chat_messages(
    db: Session,
    user_id: int,
    session_id: int,
    limit: int = 6
):
    # print("chat repository (get recent messages) -->")
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id,
        ChatMessage.session_id == session_id
    ).order_by(
        desc(ChatMessage.created_at)
    ).limit(limit).all()
    print(f"Retrieved {len(messages)} recent messages from DB")
    return list(reversed(messages))

def get_user_all_chat_messages(
    db: Session,
    user_id: int
):
    """
    Return all chat messages for current user only.
    """

    return db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(
        desc(ChatMessage.created_at)
    ).all()


def get_user_chat_message_by_id(
    db: Session,
    user_id: int,
    message_id: int
):
    """
    Return one message only if it belongs to current user.
    """

    return db.query(ChatMessage).filter(
        ChatMessage.id == message_id,
        ChatMessage.user_id == user_id
    ).first()


def delete_user_chat_message(
    db: Session,
    user_id: int,
    message_id: int
):
    """
    Delete one message only if it belongs to current user.
    """

    message = get_user_chat_message_by_id(
        db=db,
        user_id=user_id,
        message_id=message_id
    )

    if not message:
        return None

    db.delete(message)
    db.commit()

    return message