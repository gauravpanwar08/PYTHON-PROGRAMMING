# ==================================================================================================
#                       UNION, UNION ALL, INTERSECT & EXCEPT
#
# union()     → UNION     → Combines query results and removes duplicate rows.
# union_all() → UNION ALL → Combines query results and keeps duplicate rows.
# intersect() → INTERSECT → Returns rows that exist in both queries.
# except_()   → EXCEPT    → Returns rows that exist in the first query but not in the second query.
# ====================================================================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    select,
    union,
    union_all,
    intersect,
    except_,
)


# Create engine
engine = create_engine("sqlite:///union_and_intersect.db")

metadata = MetaData()


employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
)


contractors = Table(
    "contractors",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
)


metadata.create_all(engine)


employee_data = [
    {"id": 1, "name": "Gaurav"},
    {"id": 2, "name": "Rahul"},
    {"id": 3, "name": "Aman"},
    {"id": 4, "name": "Priya"},
]


contractor_data = [
    {"id": 101, "name": "Rahul"},
    {"id": 102, "name": "Priya"},
    {"id": 103, "name": "Neha"},
    {"id": 104, "name": "Vikas"},
]


with engine.begin() as connection:
    connection.execute(employees.insert(), employee_data)
    connection.execute(contractors.insert(), contractor_data)


# -------------------------------------------------------------------
# UNION - Combines results and removes duplicate rows.
# -------------------------------------------------------------------

employee_names = select(employees.c.name)

contractor_names = select(contractors.c.name)

stmt = union(
    employee_names,
    contractor_names,
)

with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- UNION ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# UNION ALL - Combines results and keeps duplicate rows.
# -------------------------------------------------------------------

stmt = union_all(
    employee_names,
    contractor_names,
)

with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- UNION ALL ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# INTERSECT - Returns rows that exist in both queries.
# -------------------------------------------------------------------

stmt = intersect(
    employee_names,
    contractor_names,
)

with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- INTERSECT ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# EXCEPT - Returns rows that exist in the first query but not in the second.
# -------------------------------------------------------------------

stmt = except_(
    employee_names,
    contractor_names,
)

with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- EXCEPT ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# UNION with multiple columns - Combines SELECT statements with the same column structure.
# -------------------------------------------------------------------

employee_details = select(
    employees.c.id,
    employees.c.name,
)

contractor_details = select(
    contractors.c.id,
    contractors.c.name,
)

stmt = union(
    employee_details,
    contractor_details,
)

with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- UNION WITH MULTIPLE COLUMNS ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# ORDER BY - Sorts the final combined result.
# -------------------------------------------------------------------

stmt = union(
    employee_names,
    contractor_names,
).order_by("name")

with engine.connect() as connection:
    result = connection.execute(stmt)

    print("\n--- UNION + ORDER BY ---")

    for row in result:
        print(row)


# -------------------------------------------------------------------
# Generated SQL - UNION
# -------------------------------------------------------------------

stmt = union(
    employee_names,
    contractor_names,
)

print("\n--- GENERATED SQL: UNION ---")
print(stmt)


# -------------------------------------------------------------------
# Generated SQL - UNION ALL
# -------------------------------------------------------------------

stmt = union_all(
    employee_names,
    contractor_names,
)

print("\n--- GENERATED SQL: UNION ALL ---")
print(stmt)


# -------------------------------------------------------------------
# Generated SQL - INTERSECT
# -------------------------------------------------------------------

stmt = intersect(
    employee_names,
    contractor_names,
)

print("\n--- GENERATED SQL: INTERSECT ---")
print(stmt)


# -------------------------------------------------------------------
# Generated SQL - EXCEPT
# -------------------------------------------------------------------

stmt = except_(
    employee_names,
    contractor_names,
)

print("\n--- GENERATED SQL: EXCEPT ---")
print(stmt)
