# =======================================================
# SQLALCHEMY CORE EXPRESSIONS & RAW SQL & text()
#
# - text()
# - Raw SQL SELECT
# - Raw SQL INSERT
# - Raw SQL UPDATE
# - Raw SQL DELETE
# - Named parameters
# - bindparams()
# - Safe parameter passing
# ========================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    text,
    bindparam,
)


# Create engine
engine = create_engine("sqlite:///raw_sql.db", echo=True)

# Create metadata
metadata = MetaData()


# Create users table
users = Table(
    "users",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("age", Integer, nullable=False),
)


# Create table
metadata.create_all(engine)


# Insert sample data
with engine.begin() as connection:

    connection.execute(
        users.insert(),
        [
            {"name": "Gaurav", "age": 22},
            {"name": "Priya", "age": 24},
            {"name": "Rahul", "age": 17},
        ],
    )


# -------------------------------------------------------------------
# RAW SQL SELECT
# -------------------------------------------------------------------

stmt = text(
    "SELECT * FROM users"
)

with engine.connect() as connection:

    result = connection.execute(stmt)

    for row in result:
        print(row)


# -------------------------------------------------------------------
# RAW SQL SELECT WITH PARAMETERS
# -------------------------------------------------------------------

stmt = text(
    "SELECT * FROM users WHERE age >= :min_age"
)

with engine.connect() as connection:

    result = connection.execute(
        stmt,
        {"min_age": 18},
    )

    for row in result:
        print(row)


# -------------------------------------------------------------------
# RAW SQL INSERT
# -------------------------------------------------------------------

stmt = text(
    """
    INSERT INTO users (name, age)
    VALUES (:name, :age)
    """
)

with engine.begin() as connection:

    connection.execute(
        stmt,
        {
            "name": "Aman",
            "age": 21,
        },
    )


# -------------------------------------------------------------------
# RAW SQL UPDATE
# -------------------------------------------------------------------

stmt = text(
    """
    UPDATE users
    SET age = :age
    WHERE name = :name
    """
)

with engine.begin() as connection:

    connection.execute(
        stmt,
        {
            "name": "Gaurav",
            "age": 23,
        },
    )


# -------------------------------------------------------------------
# RAW SQL DELETE
# -------------------------------------------------------------------

stmt = text(
    """
    DELETE FROM users
    WHERE name = :name
    """
)

with engine.begin() as connection:

    connection.execute(
        stmt,
        {"name": "Rahul"},
    )


# -------------------------------------------------------------------
# text() + bindparams()
# -------------------------------------------------------------------

stmt = text(
    "SELECT * FROM users WHERE age >= :min_age"
).bindparams(
    bindparam(
        "min_age",
        type_=Integer,
    )
)

with engine.connect() as connection:

    result = connection.execute(
        stmt,
        {"min_age": 18},
    )

    for row in result:
        print(row)


# -------------------------------------------------------------------
# SAFE PARAMETER PASSING
# -------------------------------------------------------------------

user_input = "Gaurav"

stmt = text(
    "SELECT * FROM users WHERE name = :name"
)

with engine.connect() as connection:

    result = connection.execute(
        stmt,
        {"name": user_input},
    )

    print(result.all())


# -------------------------------------------------------------------
# GENERATED SQL
# -------------------------------------------------------------------

print(
    stmt.compile(
        engine,
        compile_kwargs={"literal_binds": True},
    )
)