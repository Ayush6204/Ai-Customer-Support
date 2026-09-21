from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, default="New Chat", nullable=False)

    user = relationship(
        "User",
        back_populates="chat_sessions"
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan"
    )