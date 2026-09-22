# ================================================================================
#                    SQLALCHEMY + ALEMBIC — DATABASE
#
# This file contains the SQLAlchemy Engine and Declarative Base.
# Alembic will use Base.metadata to detect ORM model changes.
# ================================================================================


from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase

# create database URL

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="aura123",
    host="localhost",
    port=5432,
    database="sqlalchemy_alembic_db"
)

# Create Engine

engine = create_engine(DATABASE_URL)

# Create Declarative Base

class Base(DeclarativeBase):
    pass
