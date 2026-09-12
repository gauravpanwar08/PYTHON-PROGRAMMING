# ============================================================
#                        SELECT
#
# select()  → Creates a SELECT SQL statement
# where()   → Adds filtering conditions
# execute() → Executes the SELECT statement
# Result    → Contains rows returned by the database
# scalars() → Extracts values from the first selected column
# ============================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    insert,
    select,
)

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


# Create Table

metadata.create_all(engine)


# Insert Sample Data

with engine.begin() as connection:

    connection.execute(
        insert(users),
        [
            {"name": "Gaurav", "email": "gaurav@example.com"},
            {"name": "Rahul", "email": "rahul@example.com"},
        ],
    )


# Create SELECT Statement

stmt = select(users)


# Execute SELECT

with engine.connect() as connection:

    result = connection.execute(stmt)

    for row in result:
        print(row)
