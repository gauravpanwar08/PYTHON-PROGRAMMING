# ============================================================
#                              HAVING
#
# having() → Filters grouped/aggregate results
#
# WHERE → Filters individual rows before grouping
#
# HAVING COUNT() → Filters groups based on row count
# HAVING SUM()   → Filters groups based on total
# HAVING AVG()   → Filters groups based on average
# HAVING MIN()   → Filters groups based on minimum value
# HAVING MAX()   → Filters groups based on maximum value
#
# WHERE + GROUP BY + HAVING
# → Filters rows, creates groups, then filters groups
#
# GROUP BY + JOIN + HAVING
# → Groups joined data and filters aggregate results
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
    func,
    and_,
)

DATABASE_URL = "sqlite:///having.db"

engine = create_engine(DATABASE_URL, echo=True)

metadata = MetaData()

users = Table(
    "users", metadata, Column("id", Integer, primary_key=True), Column("name", String)
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("product", String),
    Column("amount", Integer),
)

metadata.create_all(engine)

with engine.begin() as connection:
    connection.execute(
        insert(users),
        [{"name": "Gaurav"}, {"name": "Rahul"}, {"name": "Aman"}, {"name": "Rohit"}],
    )

    connection.execute(
        insert(orders),
        [
            {"user_id": 1, "product": "Laptop", "amount": 50000},
            {"user_id": 1, "product": "Mouse", "amount": 2000},
            {"user_id": 1, "product": "Keyboard", "amount": 3000},
            {"user_id": 2, "product": "Monitor", "amount": 15000},
            {"user_id": 2, "product": "Chair", "amount": 10000},
            {"user_id": 3, "product": "Phone", "amount": 30000},
            {"user_id": 4, "product": "Book", "amount": 500},
        ],
    )


with engine.connect() as connection:

    # --------------------------------------------------------
    # HAVING COUNT()
    # Users with more than 2 orders
    # --------------------------------------------------------

    stmt = (
        select(orders.c.user_id, func.count(orders.c.id))
        .group_by(orders.c.user_id)
        .having(func.count(orders.c.id) > 2)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # HAVING SUM()
    # Users whose total order amount is greater than 30000
    # --------------------------------------------------------

    stmt = (
        select(orders.c.user_id, func.sum(orders.c.amount))
        .group_by(orders.c.user_id)
        .having(func.sum(orders.c.amount) > 30000)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # HAVING AVG()
    # Users whose average order amount is greater than 10000
    # --------------------------------------------------------

    stmt = (
        select(orders.c.user_id, func.avg(orders.c.amount))
        .group_by(orders.c.user_id)
        .having(func.avg(orders.c.amount) > 10000)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # HAVING MIN()
    # Users whose minimum order amount is greater than 1000
    # --------------------------------------------------------

    stmt = (
        select(orders.c.user_id, func.min(orders.c.amount))
        .group_by(orders.c.user_id)
        .having(func.min(orders.c.amount) > 1000)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # HAVING MAX()
    # Users whose maximum order amount is greater than 20000
    # --------------------------------------------------------

    stmt = (
        select(orders.c.user_id, func.max(orders.c.amount))
        .group_by(orders.c.user_id)
        .having(func.max(orders.c.amount) > 20000)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # WHERE + GROUP BY + HAVING
    #
    # First keep orders above 1000
    # Then group by user
    # Then keep users with more than 1 matching order
    # --------------------------------------------------------

    stmt = (
        select(orders.c.user_id, func.count(orders.c.id))
        .where(orders.c.amount > 1000)
        .group_by(orders.c.user_id)
        .having(func.count(orders.c.id) > 1)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # GROUP BY + JOIN + HAVING
    # User name + total amount
    # Only users whose total is greater than 30000
    # --------------------------------------------------------

    stmt = (
        select(users.c.name, func.sum(orders.c.amount))
        .select_from(users.join(orders, users.c.id == orders.c.user_id))
        .group_by(users.c.id, users.c.name)
        .having(func.sum(orders.c.amount) > 30000)
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)

    # --------------------------------------------------------
    # MULTIPLE HAVING CONDITIONS
    #
    # More than 1 order
    # AND total amount greater than 10000
    # --------------------------------------------------------

    stmt = (
        select(orders.c.user_id, func.count(orders.c.id), func.sum(orders.c.amount))
        .group_by(orders.c.user_id)
        .having(and_(func.count(orders.c.id) > 1, func.sum(orders.c.amount) > 10000))
    )

    result = connection.execute(stmt)

    for row in result:
        print(row)
