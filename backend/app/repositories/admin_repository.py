from sqlalchemy.orm import Session

from app.models.user import User
from app.models.document import Document
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage


def get_all_users(db: Session):
    return db.query(User).order_by(User.created_at.desc()).all()


def get_all_documents(db: Session):
    return db.query(Document).order_by(Document.created_at.desc()).all()


def get_system_logs_summary(db: Session):
    total_users = db.query(User).count()
    total_documents = db.query(Document).count()
    total_sessions = db.query(ChatSession).count()
    total_messages = db.query(ChatMessage).count()

    return {
        "total_users": total_users,
        "total_documents": total_documents,
        "total_sessions": total_sessions,
        "total_messages": total_messages,
    }