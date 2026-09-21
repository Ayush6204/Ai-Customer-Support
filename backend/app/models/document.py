from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Document(Base):
    __tablename__ = "documents"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # New: document belongs to one chat session
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)

    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    chroma_collection = Column(String, nullable=False)

    status = Column(String, default="uploaded", nullable=False)
    error_message = Column(Text, nullable=True)

    user = relationship(
        "User",
        back_populates="documents"
    )

    session = relationship(
        "ChatSession"
    )

    chat_messages = relationship(
        "ChatMessage",
        back_populates="document"
    )