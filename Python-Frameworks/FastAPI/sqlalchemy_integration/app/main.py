
# Initialize FastAPI and register the user router.

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import Base, engine
from app.db.dependencies import get_db
from app.models import User
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create missing tables for local development.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FastAPI + SQLAlchemy + PostgreSQL",
    lifespan=lifespan,
)

app.include_router(users_router)


@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL integration is working"}


@app.get("/db-check")
def check_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"database": "connected"}

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        ) from exc


@app.get("/db-session-check")
def check_db_session(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected", "session": "working"}

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database query failed",
        ) from exc
