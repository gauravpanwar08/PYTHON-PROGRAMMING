# ===============================================================================================================
#                        MAPPED + MAPPED_COLUMN
#
# Mapped[T]          : Marks a Python attribute as an ORM-mapped attribute and provides its Python type.
# mapped_column()    : Defines database column configuration for an ORM-mapped attribute.
#
# primary_key=       : Defines the column as a primary key.
# nullable=          : Controls whether NULL values are allowed.
# unique=            : Creates a unique constraint for the column.
# index=             : Creates a database index for the column.
# default=           : Defines a SQLAlchemy/Python-side default value.
# server_default=   : Defines a database/server-side default value.
#
# Common Type Mapping:
# int                → INTEGER
# str                → VARCHAR
# float              → FLOAT
# bool               → BOOLEAN
# String(100)        → VARCHAR(100)
# ===============================================================================================================


from sqlalchemy import URL, create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# -------------------------------------------------------------------
# Create database URL
# -------------------------------------------------------------------

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="aura123",
    host="localhost",
    port=5432,
    database="sqlalchemy_db",
)


# Create engine

engine = create_engine(DATABASE_URL, echo=True)


# Create Declarative Base

class Base(DeclarativeBase):
    pass

# -------------------------------------------------
# User Model
# -------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    age: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)


# Create table in database

Base.metadata.create_all(engine)


# Inspect mapped columns

print("User Columns:")

for column in User.__table__.columns:
    print(column.name, "→", column.type)
