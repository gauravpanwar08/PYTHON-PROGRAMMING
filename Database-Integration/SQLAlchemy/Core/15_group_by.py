# ===================================================================
# GROUP BY : Groups rows with the same values in one or more columns
#            so aggregate functions can be applied to each group.
#
# group_by() → Groups rows based on one or more columns
#
# count()    → Counts rows or values
# sum()      → Calculates the total
# avg()      → Calculates the average
# min()      → Returns the minimum value
# max()      → Returns the maximum value
#
# where()    → Filters individual rows
#              Used before grouping/group_by() or aggregation.
#
# having()   → Filters grouped/aggregate results
#              Used after grouping/group_by() and aggregation.
#
# GROUP BY + JOIN → Groups data from related tables
# ======================================================================


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

DATABASE_URL = "sqlite:///group_by.db"

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
    Column("amount", Integer)
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
            {"user_id": 1, "product": "Laptop", "amount": 50000},
            {"user_id": 1, "product": "Mouse", "amount": 2000},
            {"user_id": 2, "product": "Keyboard", "amount": 3000},
            {"user_id": 2, "product": "Monitor", "amount": 15000},
            {"user_id": 3, "product": "Phone", "amount": 30000}
        ]
    )


with engine.connect() as connection:

    # --------------------------------------------------------
    # COUNT
    # --------------------------------------------------------

    stmt = (
        select(
            orders.c.user_id,
            func.count()
        )
        .group_by(orders.c.user_id)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # SUM
    # --------------------------------------------------------

    stmt = (
        select(
            orders.c.user_id,
            func.sum(orders.c.amount)
        )
        .group_by(orders.c.user_id)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # AVG
    # --------------------------------------------------------

    stmt = (
        select(
            orders.c.user_id,
            func.avg(orders.c.amount)
        )
        .group_by(orders.c.user_id)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # MIN
    # --------------------------------------------------------

    stmt = (
        select(
            orders.c.user_id,
            func.min(orders.c.amount)
        )
        .group_by(orders.c.user_id)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # MAX
    # --------------------------------------------------------

    stmt = (
        select(
            orders.c.user_id,
            func.max(orders.c.amount)
        )
        .group_by(orders.c.user_id)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # HAVING
    # Users with more than 1 order
    # --------------------------------------------------------

    stmt = (
        select(
            orders.c.user_id,
            func.count()
        )
        .group_by(orders.c.user_id)
        .having(func.count() > 1)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # GROUP BY + JOIN
    # User name + total orders
    # --------------------------------------------------------

    stmt = (
        select(
            users.c.name,
            func.count(orders.c.id)
        )
        .select_from(
            users.join(
                orders,
                users.c.id == orders.c.user_id
            )
        )
        .group_by(users.c.id, users.c.name)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # GROUP BY + JOIN + SUM
    # User name + total amount spent
    # --------------------------------------------------------

    stmt = (
        select(
            users.c.name,
            func.sum(orders.c.amount)
        )
        .select_from(
            users.join(
                orders,
                users.c.id == orders.c.user_id
            )
        )
        .group_by(users.c.id, users.c.name)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

