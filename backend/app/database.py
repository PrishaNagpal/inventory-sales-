from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    """Parent class for every SQLAlchemy model (one class ≈ one table)."""


# engine = the actual connection pool to PostgreSQL
engine = create_engine(settings.database_url, pool_pre_ping=True)

# SessionLocal() gives us one "conversation" with the DB per request
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: open a session, yield it, always close it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
