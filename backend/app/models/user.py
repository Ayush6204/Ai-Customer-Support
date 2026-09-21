from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    documents = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    chat_sessions = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    chat_messages = relationship(
        "ChatMessage",
        back_populates="user", # Ensure relationship is defined for chat messages as well 
        cascade="all, delete-orphan" # Ensure messages are deleted if user is deleted
    )