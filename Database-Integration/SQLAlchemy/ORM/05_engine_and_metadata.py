# ===============================================================================================================
#                                ENGINE + METADATA
#
# Engine        : SQLAlchemy interface responsible for database connectivity and communication.
#                 Also handles connection pooling and transaction management.

# MetaData      : Collection of database schema information such as tables, columns and constraints.
#                 Also provides methods to create and drop tables in the database.
#
# Base.metadata : MetaData associated with the DeclarativeBase containing ORM model table definitions.
# create_engine(): Creates a SQLAlchemy Engine using the database connection configuration.
# create_all()  : Creates tables registered in the metadata if they do not already exist.
# ===============================================================================================================


from sqlalchemy import URL, create_engine
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


# -------------------------------------------------------------------
# create_engine() - Creates the SQLAlchemy Engine for database communication.
# -------------------------------------------------------------------

engine = create_engine(DATABASE_URL, echo=True)


# -------------------------------------------------------------------
# DeclarativeBase - Base class used for SQLAlchemy ORM models.
# -------------------------------------------------------------------


class Base(DeclarativeBase):
    pass


# User model


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


# Product model


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]


# Show metadata information

print("Metadata:")
print(Base.metadata)

print("\nRegistered Tables:")

for table_name in Base.metadata.tables:
    print(table_name)


# -------------------------------------------------------------------
# create_all() - Creates registered tables in the database if they do not exist.
# -------------------------------------------------------------------

Base.metadata.create_all(engine)


# Show underlying Core Table objects

print("\nUser Table:")
print(User.__table__)

print("\nProduct Table:")
print(Product.__table__)
