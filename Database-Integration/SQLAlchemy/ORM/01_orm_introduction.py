# ========================================================================================================================
#          SQLAlchemy ORM Introduction
''' 
SQLAlchemy ORM is an Object-Relational Mapping system that maps Python classes and objects to database tables and rows.

SQLAlchemy ORM allows to interact or work with relational databases data using Python classes, objects and ORM operations. 
instead of writing SQL queries for every database operation.
'''

# Database                 Python
# ────────────────────────────────────
# Table          ↔         Class/Model
# Column         ↔         Attribute
# Row            ↔         Object
# Relationship   ↔         relationship()
# =========================================================================================================================


from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# Database Configuration

engine = create_engine(
    "postgresql+psycopg://postgres:aura123@localhost:5432/sqlalchemy_db",
    echo=True
)


# ORM Base

class Base(DeclarativeBase):
    pass


# User Model

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str] = mapped_column(
        String(255)
    )


# Create Table

Base.metadata.create_all(engine)


# Create ORM Object

user = User(
    name="Gaurav",
    email="gaurav@gmail.com"
)


# Add Object Using Session

with Session(engine) as session:
    session.add(user)
    session.commit()


# Read ORM Object

with Session(engine) as session:
    stmt = select(User).where(
        User.name == "Gaurav"
    )

    result = session.scalars(stmt).first()

    print(result.name)
    print(result.email)
