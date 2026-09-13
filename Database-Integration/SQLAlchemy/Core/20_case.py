# ===================================================================================================
#                                           CASE
# Creates conditional logic in a SQL query, returning different values based on specified conditions.
#
# case() → Creates a SQL CASE expression
# syntax → case(
#              (condition, result),
#              (condition, result),
#              else_=default_result
#          )
#
# WHEN ... THEN → Defines a condition and its result
# ELSE → Defines the result when no condition matches
#
# CASE + SELECT   → Adds conditional values to query results
# CASE + func     → Uses CASE inside aggregate functions
# CASE + ORDER BY → Sorts rows using conditional logic
# CASE + GROUP BY → Groups rows based on a calculated condition
# ====================================================================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    insert,
    select,
    case,
    func,
)

DATABASE_URL = "sqlite:///case.db"

engine = create_engine(DATABASE_URL, echo=True)

metadata = MetaData()

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer", String),
    Column("amount", Integer),
    Column("status", String),
)

metadata.create_all(engine)

with engine.begin() as connection:
    connection.execute(
        insert(orders),
        [
            {"customer": "Gaurav", "amount": 50000, "status": "completed"},
            {"customer": "Rahul", "amount": 15000, "status": "completed"},
            {"customer": "Aman", "amount": 3000, "status": "pending"},
            {"customer": "Rohit", "amount": 8000, "status": "cancelled"},
            {"customer": "Neha", "amount": 25000, "status": "completed"},
        ],
    )


with engine.connect() as connection:

    # --------------------------------------------------------
    # BASIC CASE
    # Classify orders based on amount
    # --------------------------------------------------------

    order_level = case(
        (orders.c.amount >= 30000, "High"),
        (orders.c.amount >= 10000, "Medium"),
        else_= "Low",
    )

    stmt = select(orders.c.customer, orders.c.amount, order_level.label("order_level"))

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # CASE WITH STATUS
    # Convert status into a readable label
    # --------------------------------------------------------

    status_label = case(
        (orders.c.status == "completed", "Order Completed"),
        (orders.c.status == "pending", "Order Pending"),
        (orders.c.status == "cancelled", "Order Cancelled"),
        else_="Unknown",
    )

    stmt = select(
        orders.c.customer, orders.c.status, status_label.label("status_label")
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # CASE + FUNC
    # Count high-value orders
    # --------------------------------------------------------

    high_value = case((orders.c.amount >= 30000, 1), else_=0)

    stmt = select(func.sum(high_value).label("high_value_orders"))

    result = connection.execute(stmt)

    print(result.scalar())

    # --------------------------------------------------------
    # CASE + SUM
    # Total amount from completed orders
    # --------------------------------------------------------

    completed_amount = case((orders.c.status == "completed", orders.c.amount), else_=0)

    stmt = select(func.sum(completed_amount).label("completed_total"))

    result = connection.execute(stmt)

    print(result.scalar())

    # --------------------------------------------------------
    # CASE + ORDER BY
    # Completed orders first
    # --------------------------------------------------------

    status_priority = case(
        (orders.c.status == "completed", 1),
        (orders.c.status == "pending", 2),
        (orders.c.status == "cancelled", 3),
        else_=4,
    )

    stmt = select(orders.c.customer, orders.c.status, orders.c.amount).order_by(
        status_priority
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # CASE + GROUP BY
    # Group orders into High / Medium / Low
    # --------------------------------------------------------

    order_level = case(
        (orders.c.amount >= 30000, "High"),
        (orders.c.amount >= 10000, "Medium"),
        else_="Low",
    )

    stmt = select(
        order_level.label("order_level"), func.count().label("order_count")
    ).group_by(order_level)

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # CASE + GROUP BY + SUM
    # Total amount for each order level
    # --------------------------------------------------------

    order_level = case(
        (orders.c.amount >= 30000, "High"),
        (orders.c.amount >= 10000, "Medium"),
        else_="Low",
    )

    stmt = select(
        order_level.label("order_level"),
        func.count().label("order_count"),
        func.sum(orders.c.amount).label("total_amount"),
    ).group_by(order_level)

    result = connection.execute(stmt)

    for row in result:
        print(row)
