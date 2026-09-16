# ===============================================================================================================
#                             DECLARATIVE BASE
#
# DeclarativeBase : Base class used to define SQLAlchemy ORM models.
#
# Base            : Application-level base class created by inheriting from DeclarativeBase. All ORM models normally inherit from Base.
# Base.metadata   : MetaData object associated with the declarative base. It contains information about tables defined by ORM models.
# metadata.tables : Collection of tables registered inside the MetaData object.
# create_all()    : Creates all tables registered in the metadata that do not already exist.
#
# Core vs ORM:
# Core → MetaData() is generally created explicitly.
# ORM  → DeclarativeBase provides the metadata through Base.metadata.
# ===============================================================================================================


from sqlalchemy import URL, create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# -------------------------------------------------------------------
# Database Configuration
# -------------------------------------------------------------------

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="aura123",
    host="localhost",
    port=5432,
    database="sqlalchemy_db",
)

# -------------------------------------------------------------------
# Create engine
# -------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=True
)


# -------------------------------------------------------------------
# Create Declarative Base
# -------------------------------------------------------------------


class Base(DeclarativeBase):
    pass


# User Model


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255))


# Product Model


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float]


# Check tables registered in Base.metadata

print("Registered Tables:")

for table_name in Base.metadata.tables:
    print(table_name)


# Create tables in database

Base.metadata.create_all(engine)
