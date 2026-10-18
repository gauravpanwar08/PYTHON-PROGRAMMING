# Configure the SQLAlchemy engine, sessions, and ORM base class.

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# Database Engine
# Manages connections between the application and PostgreSQL

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


# Session Factory
# Creates database sessions for individual operations or requests

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# ORM Base Class
# All SQLAlchemy ORM models will inherit from this class.

class Base(DeclarativeBase):
    pass
