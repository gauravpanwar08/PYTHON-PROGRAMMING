# ============================================================
#                                               LIMIT & OFFSET
#
# limit()  → Limits the maximum number of rows returned
#
# offset() → Skips a specified number of rows
#
# limit + offset → Commonly used for pagination
#
# Pagination:
# page 1 → offset 0
# page 2 → offset 5
# page 3 → offset 10
# ============================================================

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    insert,
    select
)

DATABASE_URL = "sqlite:///example.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String)
)

metadata.create_all(engine)

with engine.begin() as connection:
    connection.execute(
        insert(users),
        [
            {
                "name": "Gaurav",
                "email": "gaurav@example.com"
            },
            {
                "name": "Rahul",
                "email": "rahul@example.com"
            },
            {
                "name": "Aman",
                "email": "aman@example.com"
            },
            {
                "name": "Rohit",
                "email": "rohit@example.com"
            },
            {
                "name": "Priya",
                "email": "priya@example.com"
            }
        ]
    )


with engine.connect() as connection:

    # --------------------------------------------------------
    # 1. limit()
    # --------------------------------------------------------

    stmt = select(users).limit(2)

    result = connection.execute(stmt)

    print("\nlimit(2):")
    print(result.all())


    # --------------------------------------------------------
    # 2. offset()
    # --------------------------------------------------------

    stmt = select(users).offset(2)

    result = connection.execute(stmt)

    print("\noffset(2):")
    print(result.all())


    # --------------------------------------------------------
    # 3. limit() + offset()
    # --------------------------------------------------------

    stmt = (
        select(users)
        .limit(2)
        .offset(2)
    )

    result = connection.execute(stmt)

    print("\nlimit(2) + offset(2):")
    print(result.all())


    # --------------------------------------------------------
    # 4. ORDER BY + LIMIT
    # --------------------------------------------------------

    stmt = (
        select(users)
        .order_by(users.c.name)
        .limit(3)
    )

    result = connection.execute(stmt)

    print("\nORDER BY + LIMIT:")
    print(result.all())


    # --------------------------------------------------------
    # 5. Pagination example
    # --------------------------------------------------------

    page = 2
    per_page = 2

    offset_value = (page - 1) * per_page

    stmt = (
        select(users)
        .order_by(users.c.id)
        .limit(per_page)
        .offset(offset_value)
    )

    result = connection.execute(stmt)

    print("\nPage 2:")
    print(result.all())
