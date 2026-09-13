# ===============================================================================================================
#                           SQL INJECTION
#
# SQL Injection → A security vulnerability/attack where untrusted input changes the structure of a SQL query.
#
# Unsafe Query : User input is directly inserted into the SQL string.
# Safe Query   : User input is passed separately as a bound parameter.
#
# text()       → Creates a textual SQL statement.
# bindparam()  → Creates a named parameter for a SQL expression.
#
# Prevention:
#   - Use parameterized queries.
#   - Never directly concatenate or interpolate untrusted input into SQL.
# ===============================================================================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    select,
    text,
)


# Create engine
engine = create_engine("sqlite:///sql_injection.db")

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
# UNSAFE QUERY - Directly inserting user input into SQL.
# -------------------------------------------------------------------

user_input = "Gaurav"

unsafe_sql = f"SELECT * FROM users WHERE name = '{user_input}'"

# Execute unsafe query
with engine.connect() as connection:
    result = connection.execute(
        text(unsafe_sql)
    )

    for row in result:
        print(row)


# Generated SQL
print(unsafe_sql)


# -------------------------------------------------------------------
# SQL INJECTION - Malicious input can change the query structure.
# -------------------------------------------------------------------

malicious_input = "' OR '1'='1"

unsafe_sql = (
    f"SELECT * FROM users "
    f"WHERE name = '{malicious_input}'"
)

# Generated SQL
print(unsafe_sql)


# -------------------------------------------------------------------
# SAFE QUERY - Use a bound parameter instead of string interpolation.
# -------------------------------------------------------------------

user_input = "' OR '1'='1"

safe_sql = text(
    "SELECT * FROM users WHERE name = :name"
)

# Execute safe query
with engine.connect() as connection:
    result = connection.execute(
        safe_sql,
        {"name": user_input}
    )

    for row in result:
        print(row)


# Generated SQL
print(safe_sql)


# -------------------------------------------------------------------
# SAFE SQLAlchemy CORE - Use SQLAlchemy expressions with parameters.
# -------------------------------------------------------------------

user_input = "' OR '1'='1"

stmt = select(users).where(
    users.c.name == user_input
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)
