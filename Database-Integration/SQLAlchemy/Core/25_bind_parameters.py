# ===============================================================================================================
#              BIND PARAMETERS & PARAMETERIZED QUERIES
#
# bindparam()  → Creates a named parameter for a SQL expression. value can be supplied at execution time.
# .params()   → Assigns values to bind parameters in a statement.
#
# Benefits:
#   - Safe handling of user input
#   - Helps prevent SQL injection
#   - Reusable SQL statements
#   - Useful for dynamic queries
# ===============================================================================================================

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    select,
    bindparam,
)

# Create engine
engine = create_engine("sqlite:///bind_parameters.db")

# Create metadata
metadata = MetaData()


# Create users table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
)


# Create table in database
metadata.create_all(engine)


# Insert sample data
user_data = [
    {"id": 1, "name": "Gaurav"},
    {"id": 2, "name": "Rahul"},
    {"id": 3, "name": "Aman"},
]

with engine.begin() as connection:
    connection.execute(users.insert(), user_data)


# -------------------------------------------------------------------
# bindparam() - Create a named parameter.
# -------------------------------------------------------------------

name_param = bindparam("name")

stmt = select(users).where(users.c.name == name_param)

# Execute query with parameter
with engine.connect() as connection:
    result = connection.execute(stmt, {"name": "Gaurav"})

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# Multiple Parameters - Bind more than one value.
# -------------------------------------------------------------------

id_param = bindparam("user_id")
name_param = bindparam("name")

stmt = select(users).where(
    users.c.id == id_param,
    users.c.name == name_param,
)

# Execute query with parameters
with engine.connect() as connection:
    result = connection.execute(
        stmt,
        {
            "user_id": 1,
            "name": "Gaurav",
        },
    )

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# bindparam() with a default value.
# -------------------------------------------------------------------

name_param = bindparam(
    "name",
    value="Gaurav",
)

stmt = select(users).where(users.c.name == name_param)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# params() - Assign values to bind parameters in a statement.
# -------------------------------------------------------------------

name_param = bindparam("name")

stmt = select(users).where(
    users.c.name == name_param
)

stmt = stmt.params(
    name="Gaurav"
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# BOUND PARAMETER - Reuse the same statement with different values.
# -------------------------------------------------------------------

name_param = bindparam("search_name")

stmt = select(users).where(
    users.c.name == name_param
)

# Execute with first value
with engine.connect() as connection:
    result = connection.execute(
        stmt,
        {"search_name": "Gaurav"}
    )

    for row in result:
        print(row)

# Execute the same statement with another value
with engine.connect() as connection:
    result = connection.execute(
        stmt,
        {"search_name": "Rahul"}
    )

    for row in result:
        print(row)


# Generated SQL
print(stmt)


