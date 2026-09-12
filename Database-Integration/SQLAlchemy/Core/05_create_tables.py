# ============================================================
#                         CREATE TABLES
#
# create_all() → Creates all registered tables in the database
# bind         → Specifies the Engine/database connection
# checkfirst   → Checks whether tables already exist
#
# SQLAlchemy generates CREATE TABLE SQL from Table definitions
# =============================================================


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# SQLite Database URL

DATABASE_URL = "sqlite:///example.db"


# Create Engine

engine = create_engine(DATABASE_URL)


# Create Metadata

metadata = MetaData()


# Define Users Table

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
)


# Create Tables

metadata.create_all(
    tables=[users],        # Specifies the tables to create - If not specified, all registered tables will be created
    bind = engine,         # Binds the metadata to the engine/database connection
    checkfirst = True,     # Checks whether tables already exist - Default behavior is True
    )


print("Tables created successfully")
