from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    jti = Column(String, unique=True, index=True, nullable=False)
    token_type = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User")