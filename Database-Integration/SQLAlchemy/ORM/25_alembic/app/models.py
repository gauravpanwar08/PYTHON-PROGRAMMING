# ================================================================================
#                    SQLALCHEMY + ALEMBIC — MODELS
#
# These ORM models define the current desired database schema.
# Alembic uses Base.metadata to detect schema changes.
# ================================================================================

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

# User ORM model

class User(Base):
    __tablename__ = "alembic_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int]
    