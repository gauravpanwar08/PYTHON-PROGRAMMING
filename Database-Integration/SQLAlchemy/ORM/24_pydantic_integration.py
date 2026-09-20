# =========================================================================================
#                       SQLALCHEMY ORM — PYDANTIC INTEGRATION
# =========================================================================================


from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# Database URL
DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5432/sqlalchemy_db"


# Create engine
engine = create_engine(DATABASE_URL, echo=True)


# DeclarativeBase
class Base(DeclarativeBase):
    pass


# ---------------------
# SQLAlchemy ORM Model
# ---------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    age: Mapped[Optional[int]] = mapped_column(nullable=True)


# Create table
Base.metadata.create_all(engine)


# ------------------
# Pydantic Schema
# ------------------
class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None

    # Allow Pydantic to read data from ORM objects
    model_config = ConfigDict(from_attributes=True)


# Create User
with Session(engine) as session:
    user = User(
        name="Gaurav",
        email="gaurav@example.com",
        age=22
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    print("\nSQLAlchemy ORM Object:")
    print(user)

    # Convert ORM object → Pydantic object
    user_schema = UserSchema.model_validate(user)

    print("\nPydantic Object:")
    print(user_schema)

    print("\nPydantic Dictionary:")
    print(user_schema.model_dump())

    print("\nPydantic JSON:")
    print(user_schema.model_dump_json())
