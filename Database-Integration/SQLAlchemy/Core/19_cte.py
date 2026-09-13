# ==============================================================================================================
#                    CTE - (Common Table Expressions)
# Creates a temporary named query result set using WITH...AS, which can be referenced in the main/another query.
#
# WITH ... AS → SQL syntax generated for a CTE
# Multiple CTEs → Uses more than one CTE in a query
# cte() → Converts a SELECT statement into a CTE
#
# CTE + SELECT
# CTE + WHERE
# CTE + JOIN
# CTE + GROUP BY
# CTE + HAVING
#
# ============================================================

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

DATABASE_URL = "sqlite:///cte.db"

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
    # BASIC CTE
    # User IDs that have orders
    # --------------------------------------------------------

    ordered_users = (
        select(
            orders.c.user_id
        )
        .distinct()
        .cte("ordered_users")
    )

    stmt = select(ordered_users)

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # CTE + WHERE
    # Users whose total order amount is greater than 20000
    # --------------------------------------------------------

    user_totals = (
        select(
            orders.c.user_id,
            func.sum(orders.c.amount).label("total_amount")
        )
        .group_by(orders.c.user_id)
        .cte("user_totals")
    )

    stmt = (
        select(
            user_totals.c.user_id,
            user_totals.c.total_amount
        )
        .where(
            user_totals.c.total_amount > 20000
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # CTE + JOIN
    # User name + total order amount
    # --------------------------------------------------------

    user_totals = (
        select(
            orders.c.user_id,
            func.sum(orders.c.amount).label("total_amount")
        )
        .group_by(orders.c.user_id)
        .cte("user_totals")
    )

    stmt = (
        select(
            users.c.name,
            user_totals.c.total_amount
        )
        .select_from(
            users.join(
                user_totals,
                users.c.id == user_totals.c.user_id
            )
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # CTE + HAVING
    # Users with more than 1 order
    # --------------------------------------------------------

    user_order_counts = (
        select(
            orders.c.user_id,
            func.count(orders.c.id).label("order_count")
        )
        .group_by(orders.c.user_id)
        .having(
            func.count(orders.c.id) > 1
        )
        .cte("user_order_counts")
    )

    stmt = (
        select(
            users.c.name,
            user_order_counts.c.order_count
        )
        .select_from(
            users.join(
                user_order_counts,
                users.c.id == user_order_counts.c.user_id
            )
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # CTE + GROUP BY
    # Calculate total amount per user
    # --------------------------------------------------------

    user_totals = (
        select(
            orders.c.user_id,
            func.sum(orders.c.amount).label("total_amount")
        )
        .group_by(orders.c.user_id)
        .cte("user_totals")
    )

    stmt = (
        select(
            user_totals.c.user_id,
            func.avg(user_totals.c.total_amount)
        )
        .group_by(user_totals.c.user_id)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)


    # --------------------------------------------------------
    # MULTIPLE CTEs
    #
    # First CTE → Total amount per user
    # Second CTE → Users with total greater than 20000
    # --------------------------------------------------------

    user_totals = (
        select(
            orders.c.user_id,
            func.sum(orders.c.amount).label("total_amount")
        )
        .group_by(orders.c.user_id)
        .cte("user_totals")
    )

    high_value_users = (
        select(
            user_totals.c.user_id,
            user_totals.c.total_amount
        )
        .where(
            user_totals.c.total_amount > 20000
        )
        .cte("high_value_users")
    )

    stmt = (
        select(
            users.c.name,
            high_value_users.c.total_amount
        )
        .select_from(
            users.join(
                high_value_users,
                users.c.id == high_value_users.c.user_id
            )
        )
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)
