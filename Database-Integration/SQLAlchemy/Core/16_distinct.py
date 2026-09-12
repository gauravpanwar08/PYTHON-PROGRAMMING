# =================================================================================
# DISTINCT : Returns only unique values by removing duplicate rows from the result.
#
# distinct() → Removes duplicate result combinations
#
# SELECT DISTINCT → Returns unique values/combinations
# COUNT(DISTINCT ...) → Counts unique values
# DISTINCT + WHERE → Filters rows before returning unique values
# DISTINCT + ORDER BY → Returns unique results in sorted order
# ===================================================================================

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    insert,
    select,
    func
)

DATABASE_URL = "sqlite:///distinct.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("product", String),
    Column("category", String)
)

metadata.create_all(engine)

with engine.begin() as connection:
    connection.execute(
        insert(users),
        [
            {"name": "Gaurav"},
            {"name": "Rahul"},
            {"name": "Aman"}
        ]
    )

    connection.execute(
        insert(orders),
        [
            {"user_id": 1, "product": "Laptop", "category": "Electronics"},
            {"user_id": 1, "product": "Mouse", "category": "Electronics"},
            {"user_id": 2, "product": "Keyboard", "category": "Electronics"},
            {"user_id": 2, "product": "Chair", "category": "Furniture"},
            {"user_id": 3, "product": "Laptop", "category": "Electronics"}
        ]
    )


with engine.connect() as connection:

    # --------------------------------------------------------
    # DISTINCT
    # Unique user IDs
    # --------------------------------------------------------

    stmt = (
        select(orders.c.user_id)
        .distinct()
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # DISTINCT CATEGORY
    # --------------------------------------------------------

    stmt = (
        select(orders.c.category)
        .distinct()
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # COUNT(DISTINCT)
    # Number of unique users
    # --------------------------------------------------------

    stmt = select(
        func.count(orders.c.user_id.distinct())
    )

    result = connection.execute(stmt)

    print(result.scalar())


    # --------------------------------------------------------
    # DISTINCT WITH MULTIPLE COLUMNS
    # Unique category + product combinations
    # --------------------------------------------------------

    stmt = (
        select(
            orders.c.category,
            orders.c.product
        )
        .distinct()
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # DISTINCT + WHERE
    # Unique products in Electronics category
    # --------------------------------------------------------

    stmt = (
        select(orders.c.product)
        .where(
            orders.c.category == "Electronics"
        )
        .distinct()
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # DISTINCT + ORDER BY
    # Unique categories in alphabetical order
    # --------------------------------------------------------

    stmt = (
        select(orders.c.category)
        .distinct()
        .order_by(orders.c.category)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)
