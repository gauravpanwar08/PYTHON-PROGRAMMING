# ==========================================================================================
#                               SUBQUERY
# A query written inside another SQL query to provide data or a result for the outer query.
#
# subquery()          → Subquery used like a table
# scalar_subquery()   → Subquery used like a single value
# exists()            → Checks whether a matching row exists
#
# IN + Subquery       → Filters rows using values returned by a subquery
# Subquery in FROM    → Uses a subquery as a temporary result table
# Subquery + GROUP BY → Performs aggregation inside a subquery
# Subquery + JOIN     → Joins a table with a subquery
# ============================================================================================


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
    func,
    exists
)

DATABASE_URL = "sqlite:///subqueries.db"

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
            {"name": "Aman"},
            {"name": "Rohit"}
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
    # IN + SUBQUERY
    #
    # Find users who have placed at least one order
    # --------------------------------------------------------

    subquery = (
        select(orders.c.user_id)
        .distinct()
    )

    stmt = (
        select(users)
        .where(
            users.c.id.in_(subquery)
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # ----------------------------------------------------------
    # SUBQUERY WITH GROUP BY
    #
    # Find users whose total order amount is greater than 20000
    # ----------------------------------------------------------

    subquery = (
        select(
            orders.c.user_id
        )
        .group_by(orders.c.user_id)
        .having(
            func.sum(orders.c.amount) > 20000
        )
    )

    stmt = (
        select(users)
        .where(
            users.c.id.in_(subquery)
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # ------------------------------------------------------------------
    # SCALAR SUBQUERY
    #
    # Find orders whose amount is greater than the average order amount
    # ------------------------------------------------------------------

    average_amount = (
        select(
            func.avg(orders.c.amount)
        )
        .scalar_subquery()
    )

    stmt = (
        select(
            orders.c.product,
            orders.c.amount
        )
        .where(
            orders.c.amount > average_amount
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # EXISTS
    #
    # Find users who have at least one order
    # --------------------------------------------------------

    order_exists = (
        select(orders.c.id)
        .where(
            orders.c.user_id == users.c.id
        ).exists()
    )
      
    stmt = (
        select(users)
        .where(order_exists)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # SUBQUERY IN FROM
    #
    # Calculate total order amount per user first
    # --------------------------------------------------------

    totals = (
        select(
            orders.c.user_id,
            func.sum(orders.c.amount).label("total_amount")
        )
        .group_by(orders.c.user_id)
        .subquery()
    )

    stmt = (
        select(
            totals.c.user_id,
            totals.c.total_amount
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # SUBQUERY + JOIN
    #
    # User name + total order amount
    # --------------------------------------------------------

    totals = (
        select(
            orders.c.user_id,
            func.sum(orders.c.amount).label("total_amount")
        )
        .group_by(orders.c.user_id)
        .subquery()
    )

    stmt = (
        select(
            users.c.name,
            totals.c.total_amount
        )
        .select_from(
            users.join(
                totals,
                users.c.id == totals.c.user_id
            )
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # SUBQUERY + JOIN + FILTER
    #
    # Users whose total order amount is greater than 20000
    # --------------------------------------------------------

    totals = (
        select(
            orders.c.user_id,
            func.sum(orders.c.amount).label("total_amount")
        )
        .group_by(orders.c.user_id)
        .subquery()
    )

    stmt = (
        select(
            users.c.name,
            totals.c.total_amount
        )
        .select_from(
            users.join(
                totals,
                users.c.id == totals.c.user_id
            )
        )
        .where(
            totals.c.total_amount > 20000
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)
