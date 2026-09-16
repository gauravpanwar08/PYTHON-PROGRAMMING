# ===============================================================================================================
#                               ORM MODELS
#
# ORM Model     : A Python class mapped to a database table.
# __tablename__ : Defines the database table name for the ORM model.
# __table__     : Provides the underlying SQLAlchemy Core Table object of the ORM model.
# Base          : Declarative base from which ORM models inherit.
# Model Object  : An instance of an ORM model representing a database row.
# ===============================================================================================================


from sqlalchemy import URL, create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Database configuration

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="aura123",
    host="localhost",
    port=5432,
    database="sqlalchemy_db",
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)


# -------------------------------------------------------------------
# DeclarativeBase - Base class used for SQLAlchemy ORM models.
# -------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# User ORM model

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )


# Product ORM model

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        nullable=False
    )


# -------------------------------------------------------------------
# Base.metadata.create_all() - Creates tables registered in the metadata.
# -------------------------------------------------------------------

Base.metadata.create_all(engine)


# -------------------------------------------------------------------
# __table__ - Provides the underlying Core Table object of a model.
# -------------------------------------------------------------------

print("User Table:")
print(type(User.__table__))

print("\nProduct Table:")
print(Product.__table__)


# Show model columns

print("\nUser Columns:")

for column in User.__table__.columns:
    print(column.name, "→", column.type)


# -------------------------------------------------------------------
# ORM Object - Creates a Python object representing a database row.
# -------------------------------------------------------------------

user = User(
    name="Gaurav",
    email="gaurav@gmail.com"
)

product = Product(
    name="Laptop",
    price=75000.00
)

print("\nUser Object:")
print(user)

print("\nProduct Object:")
print(product)
