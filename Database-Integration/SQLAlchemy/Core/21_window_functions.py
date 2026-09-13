# ===============================================================================================================
# WINDOW FUNCTIONS
#
# Window Function : Performs a calculation across a set of related rows without collapsing those rows.
#
# over()          → Defines the window for a window function.
# row_number()    → Assigns a unique sequential number to each row.
# rank()          → Assigns the same rank to tied rows and leaves gaps after ties.
# dense_rank()    → Assigns the same rank to tied rows without leaving gaps.
# partition_by()  → Divides rows into separate windows.
# order_by=       → Defines the order in which the window function performs its calculation.
#
# Window Function vs GROUP BY:
# GROUP BY        → Combines rows into groups and returns one row per group.
# Window Function → Performs calculations while keeping the original rows.
# ===============================================================================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    select,
    func,
)


# Create engine
engine = create_engine("sqlite:///window_functions.db")

# Create metadata
metadata = MetaData()


# Create orders table
orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("product", String(100), nullable=False),
    Column("amount", Float, nullable=False),
)

# Create table in database
metadata.create_all(engine)


# Insert sample data
sample_orders = [
    {"user_id": 1, "product": "Laptop", "amount": 80000},
    {"user_id": 1, "product": "Mouse", "amount": 2000},
    {"user_id": 1, "product": "Keyboard", "amount": 5000},
    {"user_id": 2, "product": "Monitor", "amount": 15000},
    {"user_id": 2, "product": "Headphones", "amount": 5000},
    {"user_id": 2, "product": "Webcam", "amount": 3000},
    {"user_id": 3, "product": "Phone", "amount": 60000},
    {"user_id": 3, "product": "Charger", "amount": 2000},
]

with engine.begin() as connection:
    connection.execute(orders.insert(), sample_orders)


# -------------------------------------------------------------------
# over() - Defines the window used by a window function.
# -------------------------------------------------------------------

stmt = select(
    orders.c.product,
    orders.c.amount,
    func.sum(orders.c.amount).over().label("total_amount"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- over() ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# ROW_NUMBER() - Assigns a unique sequential number to each row.
# -------------------------------------------------------------------

stmt = select(
    orders.c.id,
    orders.c.product,
    orders.c.amount,
    func.row_number().over(
        order_by=orders.c.amount.desc()
    ).label("row_number"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- ROW_NUMBER() ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# RANK() - Assigns the same rank to tied rows and leaves gaps after ties.
# -------------------------------------------------------------------

stmt = select(
    orders.c.product,
    orders.c.amount,
    func.rank().over(
        order_by=orders.c.amount.desc()
    ).label("rank"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- RANK() ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# DENSE_RANK() - Assigns the same rank to tied rows without leaving gaps.
# -------------------------------------------------------------------

stmt = select(
    orders.c.product,
    orders.c.amount,
    func.dense_rank().over(
        order_by=orders.c.amount.desc()
    ).label("dense_rank"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- DENSE_RANK() ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# PARTITION BY - Divides rows into separate windows.
# -------------------------------------------------------------------

stmt = select(
    orders.c.user_id,
    orders.c.product,
    orders.c.amount,
    func.row_number().over(
        partition_by=orders.c.user_id,
        order_by=orders.c.amount.desc(),
    ).label("user_row_number"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- ROW_NUMBER() + PARTITION BY ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# RANK() + PARTITION BY - Ranks rows separately inside each partition.
# -------------------------------------------------------------------

stmt = select(
    orders.c.user_id,
    orders.c.product,
    orders.c.amount,
    func.rank().over(
        partition_by=orders.c.user_id,
        order_by=orders.c.amount.desc(),
    ).label("user_rank"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- RANK() + PARTITION BY ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# DENSE_RANK() + PARTITION BY - Ranks rows separately without rank gaps.
# -------------------------------------------------------------------

stmt = select(
    orders.c.user_id,
    orders.c.product,
    orders.c.amount,
    func.dense_rank().over(
        partition_by=orders.c.user_id,
        order_by=orders.c.amount.desc(),
    ).label("user_dense_rank"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- DENSE_RANK() + PARTITION BY ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# RUNNING SUM - Calculates a cumulative sum while keeping every row.
# -------------------------------------------------------------------

stmt = select(
    orders.c.id,
    orders.c.product,
    orders.c.amount,
    func.sum(orders.c.amount).over(
        order_by=orders.c.id
    ).label("running_total"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- RUNNING SUM ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# RUNNING AVG - Calculates a cumulative average while keeping every row.
# -------------------------------------------------------------------

stmt = select(
    orders.c.id,
    orders.c.product,
    orders.c.amount,
    func.avg(orders.c.amount).over(
        order_by=orders.c.id
    ).label("running_average"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- RUNNING AVG ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# SUM() + PARTITION BY - Calculates each user's total while keeping every order row.
# -------------------------------------------------------------------

stmt = select(
    orders.c.user_id,
    orders.c.product,
    orders.c.amount,
    func.sum(orders.c.amount).over(
        partition_by=orders.c.user_id
    ).label("user_total"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- USER TOTAL ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# AVG() + PARTITION BY - Calculates each user's average while keeping every order row.
# -------------------------------------------------------------------

stmt = select(
    orders.c.user_id,
    orders.c.product,
    orders.c.amount,
    func.avg(orders.c.amount).over(
        partition_by=orders.c.user_id
    ).label("user_average"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- USER AVERAGE ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# GROUP BY + WINDOW FUNCTION - Calculates group totals and ranks those groups.
# -------------------------------------------------------------------

user_totals = (
    select(
        orders.c.user_id,
        func.sum(orders.c.amount).label("total_amount"),
    )
    .group_by(orders.c.user_id)
    .subquery()
)

stmt = select(
    user_totals.c.user_id,
    user_totals.c.total_amount,
    func.rank().over(
        order_by=user_totals.c.total_amount.desc()
    ).label("user_rank"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- GROUP BY + WINDOW FUNCTION ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# WINDOW FUNCTION + FILTERING - Uses a subquery to filter a window function result.
# -------------------------------------------------------------------

ranked_orders = (
    select(
        orders.c.product,
        orders.c.amount,
        func.rank().over(
            order_by=orders.c.amount.desc()
        ).label("rank"),
    )
    .subquery()
)

stmt = select(
    ranked_orders.c.product,
    ranked_orders.c.amount,
    ranked_orders.c.rank,
).where(
    ranked_orders.c.rank <= 3
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- TOP 3 USING WINDOW FUNCTION ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# WINDOW FUNCTION + PARTITION BY + ORDER BY - Ranks each user's orders by amount.
# -------------------------------------------------------------------

stmt = select(
    orders.c.user_id,
    orders.c.product,
    orders.c.amount,
    func.row_number().over(
        partition_by=orders.c.user_id,
        order_by=orders.c.amount.desc(),
    ).label("user_order_rank"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- USER ORDER RANK ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# Generated SQL - ROW_NUMBER() with PARTITION BY and ORDER BY.
# -------------------------------------------------------------------

stmt = select(
    orders.c.user_id,
    orders.c.product,
    orders.c.amount,
    func.row_number().over(
        partition_by=orders.c.user_id,
        order_by=orders.c.amount.desc(),
    ).label("user_order_rank"),
)

print("\n--- GENERATED SQL ---")
print(stmt)
