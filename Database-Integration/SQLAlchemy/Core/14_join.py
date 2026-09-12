# ===============================================================================================================
# JOIN : JOIN is an SQL operation
#        used to combine rows from two or more tables based on a related column between them.
#
# join()        → INNER JOIN       → Returns matching rows from both tables
# outerjoin()   → LEFT OUTER JOIN  → Returns all rows from the left table and matching rows from the right table.
# outerjoin()   → RIGHT OUTER JOIN → Returns all rows from the right table and matching rows from the left table
# full=True     → FULL OUTER JOIN  → Returns all rows from both tables with NULL where no match exists.
# cross_join()  → CROSS JOIN       → Returns every possible combination of rows from both tables.
# alias()       → SELF JOIN        → Joins a table with itself to compare or relate its rows.
# ON condition  → Defines how the tables are related
# select_from() → Specifies the FROM clause
# ================================================================================================================

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
)

DATABASE_URL = "sqlite:///joins.db"

engine = create_engine(DATABASE_URL, echo=True)

metadata = MetaData()


# USERS TABLE

users = Table(
    "users", metadata, Column("id", Integer, primary_key=True), Column("name", String)
)


# ORDERS TABLE

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("product", String),
)


# EMPLOYEES TABLE
# Used for SELF JOIN

employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("manager_id", ForeignKey("employees.id")),
)


metadata.create_all(engine)


# INSERT DATA

with engine.begin() as connection:

    connection.execute(
        insert(users), [{"name": "Gaurav"}, {"name": "Rahul"}, {"name": "Aman"}]
    )

    connection.execute(
        insert(orders),
        [
            {"user_id": 1, "product": "Laptop"},
            {"user_id": 1, "product": "Mouse"},
            {"user_id": 2, "product": "Keyboard"},
        ],
    )

    connection.execute(
        insert(employees),
        [
            {"name": "Gaurav", "manager_id": None},
            {"name": "Rahul", "manager_id": 1},
            {"name": "Aman", "manager_id": 1},
        ],
    )


with engine.connect() as connection:

    # --------------------------------------------------------
    # 1. INNER JOIN -> table1.join(table2, condition)
    # --------------------------------------------------------

    stmt = select(users.c.name, orders.c.product).select_from(
        users.join(orders, users.c.id == orders.c.user_id)
    )

    result = connection.execute(stmt)

    print("\nINNER JOIN:")

    for row in result:
        print(row)

    # ----------------------------------------------------------
    # 2. LEFT OUTER JOIN -> table1.outerjoin(table2, condition)
    # ----------------------------------------------------------

    stmt = select(users.c.name, orders.c.product).select_from(
        users.outerjoin(orders, users.c.id == orders.c.user_id)
    )

    result = connection.execute(stmt)

    print("\nLEFT OUTER JOIN:")

    for row in result:
        print(row)

    # -----------------------------------------------------------
    # 3. RIGHT OUTER JOIN -> table2.outerjoin(table1, condition)
    #
    # No dedicated rightjoin() method but we can achieve the same result by reversing the tables and using outerjoin().
    # -----------------------------------------------------------

    stmt = select(orders.c.product, users.c.name).select_from(
        orders.outerjoin(users, orders.c.user_id == users.c.id)
    )

    result = connection.execute(stmt)

    print("\nRIGHT JOIN equivalent:")

    for row in result:
        print(row)

    # -----------------------------------------------------------------
    # 4. FULL OUTER JOIN -> table1.join(table2, condition, full=True)
    # -----------------------------------------------------------------

    stmt = select(users.c.name, orders.c.product).select_from(
        users.join(orders, users.c.id == orders.c.user_id, full=True)
    )

    result = connection.execute(stmt)

    print("\nFULL OUTER JOIN:")

    for row in result:
        print(row)

    # --------------------------------------------
    # 5. CROSS JOIN -> table1.cross_join(table2)
    # --------------------------------------------

    stmt = select(users.c.name, orders.c.product).select_from(users.cross_join(orders))

    result = connection.execute(stmt)

    print("\nCROSS JOIN:")

    for row in result:
        print(row)

    # --------------------------------------------------------
    # 6. SELF JOIN -> alias() + normal join()
    # --------------------------------------------------------

    employee = employees.alias("employee")
    manager = employees.alias("manager")

    stmt = select(
        employee.c.name.label("employee"), manager.c.name.label("manager")
    ).select_from(employee.join(manager, employee.c.manager_id == manager.c.id))

    result = connection.execute(stmt)

    print("\nSELF JOIN:")

    for row in result:
        print(row)
