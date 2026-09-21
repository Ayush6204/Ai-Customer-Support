from sqlalchemy import Column, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    sources = Column(JSON, nullable=True)

    user = relationship(
        "User",
        back_populates="chat_messages"
    )

    session = relationship(
        "ChatSession",
        back_populates="messages"
    )

    document = relationship(
        "Document",
        back_populates="chat_messages"
    )