from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Convert settings.DATABASE_URL to string in case it is a Pydantic PostgresDsn/AnyUrl object
db_url = str(settings.DATABASE_URL)

# Only supply SQLite-specific arguments when using SQLite
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(
    db_url,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()