
# Provide and manage SQLAlchemy database sessions for FastAPI requests.

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.database import SessionLocal


# Database Dependency
# Creates a session, provides it to the endpoint, and closes it afterward.

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
