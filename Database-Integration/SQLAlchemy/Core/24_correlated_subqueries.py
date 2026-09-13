# ===============================================================================================================
#                      CORRELATED SUBQUERIES
# A subquery that references a column from the outer query.
#
# Correlated Subquery : Inner query depends on the current row of the outer query.
# Normal Subquery     : A subquery/inner query works independently from the outer query.
#
# scalar_subquery()   → Converts a SELECT statement into a scalar SQL expression.
# exists()            → Checks whether the correlated subquery returns at least one row.
# correlate()         → Explicitly specifies which outer table a subquery should correlate with.
#
# Common Use Cases:
#                 - Count related records for every row
#                 - Find highest/lowest related value
#                 - Check whether related records exist
#                 - Compare a row with related rows
# ===============================================================================================================

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    select,
    func,
    exists,
)

# Create engine
engine = create_engine("sqlite:///correlated_subqueries.db")

# Create metadata
metadata = MetaData()


# Create users table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
)

# Create orders table
orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("product", String(100), nullable=False),
    Column("amount", Float, nullable=False),
)


# Create tables in database
metadata.create_all(engine)


# Insert sample data
user_data = [
    {"id": 1, "name": "Gaurav"},
    {"id": 2, "name": "Rahul"},
    {"id": 3, "name": "Aman"},
    {"id": 4, "name": "Priya"},
]

order_data = [
    {"id": 1, "user_id": 1, "product": "Laptop", "amount": 80000},
    {"id": 2, "user_id": 1, "product": "Mouse", "amount": 2000},
    {"id": 3, "user_id": 1, "product": "Keyboard", "amount": 5000},
    {"id": 4, "user_id": 2, "product": "Monitor", "amount": 15000},
    {"id": 5, "user_id": 2, "product": "Headphones", "amount": 5000},
    {"id": 6, "user_id": 3, "product": "Phone", "amount": 60000},
]


with engine.begin() as connection:
    connection.execute(users.insert(), user_data)
    connection.execute(orders.insert(), order_data)


# -------------------------------------------------------------------
# CORRELATE - Explicitly specify the outer table for correlation.
# -------------------------------------------------------------------

order_count_subquery = (
    select(func.count(orders.c.id))
    .where(orders.c.user_id == users.c.id)
    .correlate(users)
    .scalar_subquery()
)

stmt = select(
    users.c.name,
    order_count_subquery.label("order_count"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED SUBQUERY vs NORMAL SUBQUERY
#
# Normal Subquery     : Inner query does not depend on the outer query.
# Correlated Subquery : Inner query references a column from the outer query.
# -------------------------------------------------------------------

normal_subquery = select(func.count(orders.c.id)).scalar_subquery()

stmt = select(
    users.c.name,
    normal_subquery.label("total_orders"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED SCALAR SUBQUERY - Count orders for every user.
# -------------------------------------------------------------------

order_count_subquery = (
    select(func.count(orders.c.id))
    .where(orders.c.user_id == users.c.id)
    .scalar_subquery()
)

stmt = select(
    users.c.name,
    order_count_subquery.label("order_count"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED SCALAR SUBQUERY - Calculate total order amount for every user.
# -------------------------------------------------------------------

total_order_amount = (
    select(func.sum(orders.c.amount))
    .where(orders.c.user_id == users.c.id)
    .scalar_subquery()
)

stmt = select(
    users.c.name,
    total_order_amount.label("total_order_amount"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED SCALAR SUBQUERY - Find maximum order amount for every user.
# -------------------------------------------------------------------

max_order_amount = (
    select(func.max(orders.c.amount))
    .where(orders.c.user_id == users.c.id)
    .scalar_subquery()
)

stmt = select(
    users.c.name,
    max_order_amount.label("max_order_amount"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED EXISTS - Check whether each user has at least one order.
# -------------------------------------------------------------------

order_exists = select(orders.c.id).where(orders.c.user_id == users.c.id).exists()

stmt = select(
    users.c.name,
    order_exists.label("has_orders"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED EXISTS - Return only users who have orders.
# -------------------------------------------------------------------

order_exists = select(orders.c.id).where(orders.c.user_id == users.c.id).exists()

stmt = select(
    users.c.id,
    users.c.name,
).where(order_exists)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED EXISTS - Return users who have an order above 50000.
# -------------------------------------------------------------------

high_value_order_exists = (
    select(orders.c.id)
    .where(
        orders.c.user_id == users.c.id,
        orders.c.amount > 50000,
    )
    .exists()
)

stmt = select(
    users.c.name,
).where(high_value_order_exists)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED SUBQUERY - Compare each user's orders with their average order amount.
# -------------------------------------------------------------------

average_order_amount = (
    select(func.avg(orders.c.amount))
    .where(orders.c.user_id == users.c.id)
    .scalar_subquery()
)

stmt = select(
    users.c.name,
    average_order_amount.label("average_order_amount"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# CORRELATED SUBQUERY + WHERE - Find users whose total order amount is above 50000.
# -------------------------------------------------------------------

total_order_amount = (
    select(func.sum(orders.c.amount))
    .where(orders.c.user_id == users.c.id)
    .scalar_subquery()
)

stmt = select(
    users.c.name,
).where(total_order_amount > 50000)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)
