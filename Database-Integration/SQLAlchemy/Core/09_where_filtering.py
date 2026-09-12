# ============================================================
#                        WHERE & FILTERING
#
# where() → Adds filtering conditions to a SELECT statement
#
# Comparison operators:
# ==  → Equal
# !=  → Not equal
# >   → Greater than
# <   → Less than
# >=  → Greater than or equal
# <=  → Less than or equal
#
# and_() → Combines conditions using AND
# or_()  → Combines conditions using OR
# not_() → Negates a condition
#
# in_() → Checks whether a value exists in a list
# like() → Pattern matching
# is_(None) → Checks for NULL
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
    and_,
    or_,
    not_
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
    # 1. Equal ==
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.name == "Gaurav"
    )

    result = connection.execute(stmt)

    print("\n== Equal:")
    print(result.all())


    # --------------------------------------------------------
    # 2. Not equal !=
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.name != "Gaurav"
    )

    result = connection.execute(stmt)

    print("\n!= Not equal:")
    print(result.all())


    # --------------------------------------------------------
    # 3. Greater than >
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.id > 2
    )

    result = connection.execute(stmt)

    print("\n> Greater than:")
    print(result.all())


    # --------------------------------------------------------
    # 4. Less than <
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.id < 3
    )

    result = connection.execute(stmt)

    print("\n< Less than:")
    print(result.all())


    # --------------------------------------------------------
    # 5. Greater than or equal >=
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.id >= 2
    )

    result = connection.execute(stmt)

    print("\n>= Greater than or equal:")
    print(result.all())


    # --------------------------------------------------------
    # 6. Less than or equal <=
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.id <= 2
    )

    result = connection.execute(stmt)

    print("\n<= Less than or equal:")
    print(result.all())


    # --------------------------------------------------------
    # 7. and_()
    # --------------------------------------------------------

    stmt = select(users).where(
        and_(
            users.c.id >= 2,
            users.c.id <= 3
        )
    )

    result = connection.execute(stmt)

    print("\nand_():")
    print(result.all())


    # --------------------------------------------------------
    # 8. or_()
    # --------------------------------------------------------

    stmt = select(users).where(
        or_(
            users.c.name == "Gaurav",
            users.c.name == "Rahul"
        )
    )

    result = connection.execute(stmt)

    print("\nor_():")
    print(result.all())


    # --------------------------------------------------------
    # 9. not_()
    # --------------------------------------------------------

    stmt = select(users).where(
        not_(users.c.name == "Gaurav")
    )

    result = connection.execute(stmt)

    print("\nnot_():")
    print(result.all())


    # --------------------------------------------------------
    # 10. in_()
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.name.in_(
            ["Gaurav", "Aman"]
        )
    )

    result = connection.execute(stmt)

    print("\nin_():")
    print(result.all())


    # --------------------------------------------------------
    # 11. like()
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.name.like("G%")
    )

    result = connection.execute(stmt)

    print("\nlike():")
    print(result.all())


    # --------------------------------------------------------
    # 12. is_(None)
    # --------------------------------------------------------

    stmt = select(users).where(
        users.c.email.is_(None)
    )

    result = connection.execute(stmt)

    print("\nis_(None):")
    print(result.all())
