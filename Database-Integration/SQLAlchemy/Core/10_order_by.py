# ============================================================
#                        ORDER BY
#
# order_by() → Sorts the rows returned by a SELECT statement
#
# asc()  → Ascending order
# desc() → Descending order
#
# Multiple columns can be passed to order_by()
#
# NULLS FIRST / NULLS LAST → Controls position of NULL values
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
    asc,
    desc
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
                "email": None
            }
        ]
    )


with engine.connect() as connection:

    # --------------------------------------------------------
    # 1. Ascending order
    # --------------------------------------------------------

    stmt = select(users).order_by(
        users.c.name
    )

    result = connection.execute(stmt)

    print("\nAscending:")
    print(result.all())


    # --------------------------------------------------------
    # 2. Explicit asc()
    # --------------------------------------------------------

    stmt = select(users).order_by(
        asc(users.c.name)
    )

    result = connection.execute(stmt)

    print("\nasc():")
    print(result.all())


    # --------------------------------------------------------
    # 3. Descending order
    # --------------------------------------------------------

    stmt = select(users).order_by(
        desc(users.c.name)
    )

    result = connection.execute(stmt)

    print("\ndesc():")
    print(result.all())


    # --------------------------------------------------------
    # 4. Column.desc()
    # --------------------------------------------------------

    stmt = select(users).order_by(
        users.c.id.desc()
    )

    result = connection.execute(stmt)

    print("\nid descending:")
    print(result.all())


    # --------------------------------------------------------
    # 5. Multiple columns
    # --------------------------------------------------------

    stmt = select(users).order_by(
        users.c.name.asc(),
        users.c.id.desc()
    )

    result = connection.execute(stmt)

    print("\nMultiple columns:")
    print(result.all())


    # --------------------------------------------------------
    # 6. NULLS LAST
    # --------------------------------------------------------

    stmt = select(users).order_by(
        users.c.email.asc().nulls_last()
    )

    result = connection.execute(stmt)

    print("\nNULLS LAST:")
    print(result.all())


    # --------------------------------------------------------
    # 7. NULLS FIRST
    # --------------------------------------------------------

    stmt = select(users).order_by(
        users.c.email.asc().nulls_first()
    )

    result = connection.execute(stmt)

    print("\nNULLS FIRST:")
    print(result.all())
