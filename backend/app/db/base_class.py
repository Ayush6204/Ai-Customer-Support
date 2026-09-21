from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


class BaseModelMixin:
    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


Base = declarative_base(cls=BaseModelMixin)