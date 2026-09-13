# ===============================================================================================================
#                                  ALIAS & LABELS
#
# Alias   : Used mainly when the same table is referenced multiple times, especially in SELF JOINs.
# alias() → Creates an alternate name for a table or query.

# Label   : Used mainly to give readable names to selected columns or expressions.
# label() → Creates an alternate name for a column or SQL expression.
#
# table.alias()  → Creates an alias for a Table.
# subquery()     → Creates a named subquery that can be used like a table.
# column.label() → Gives a column/expression a temporary name.
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
)

# Create engine
engine = create_engine("sqlite:///alias_labels.db")

# Create metadata
metadata = MetaData()


# Create employees table
employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("salary", Float, nullable=False),
    Column("manager_id", Integer, ForeignKey("employees.id")),
)

# Create departments table
departments = Table(
    "departments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
)


# Create tables in database
metadata.create_all(engine)


# Insert sample data
employee_data = [
    {"id": 1, "name": "Gaurav", "salary": 90000, "manager_id": None},
    {"id": 2, "name": "Rahul", "salary": 60000, "manager_id": 1},
    {"id": 3, "name": "Aman", "salary": 55000, "manager_id": 1},
    {"id": 4, "name": "Priya", "salary": 70000, "manager_id": 1},
    {"id": 5, "name": "Neha", "salary": 50000, "manager_id": 2},
]

department_data = [
    {"id": 1, "name": "Backend"},
    {"id": 2, "name": "Frontend"},
    {"id": 3, "name": "HR"},
]


with engine.begin() as connection:
    connection.execute(employees.insert(), employee_data)
    connection.execute(departments.insert(), department_data)


# -------------------------------------------------------------------
# ALIAS - Creates an alternate name for a table.
# -------------------------------------------------------------------

employees_alias = employees.alias("e")

stmt = select(
    employees_alias.c.id,
    employees_alias.c.name,
    employees_alias.c.salary,
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# ALIAS - Useful when the same table is referenced multiple times.
# -------------------------------------------------------------------

employees_1 = employees.alias("e1")
employees_2 = employees.alias("e2")

stmt = select(
    employees_1.c.name.label("employee_name"),
    employees_2.c.name.label("manager_name"),
).join(
    employees_2,
    employees_1.c.manager_id == employees_2.c.id,
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# SELF JOIN - Joining a table with itself using aliases.
# -------------------------------------------------------------------

employee = employees.alias("employee")
manager = employees.alias("manager")

stmt = select(
    employee.c.name.label("employee_name"),
    manager.c.name.label("manager_name"),
).join(
    manager,
    employee.c.manager_id == manager.c.id,
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# LABEL - Gives a column an alternate name.
# -------------------------------------------------------------------

stmt = select(
    employees.c.name.label("employee_name"),
    employees.c.salary.label("employee_salary"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# LABEL - Gives an expression an alternate name.
# -------------------------------------------------------------------

salary_with_bonus = (employees.c.salary * 1.10).label("salary_with_bonus")

stmt = select(
    employees.c.name,
    employees.c.salary,
    salary_with_bonus,
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# LABEL - Using aggregate function with a label.
# -------------------------------------------------------------------

total_salary = func.sum(employees.c.salary).label("total_salary")

stmt = select(total_salary)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    print(result.first())


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# LABEL - GROUP BY with a labeled expression.
# -------------------------------------------------------------------

employee_count = func.count(employees.c.id).label("employee_count")

stmt = select(
    employees.c.manager_id,
    employee_count,
).group_by(employees.c.manager_id)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# LABEL - ORDER BY using a label name.
# -------------------------------------------------------------------

salary_label = employees.c.salary.label("employee_salary")

stmt = select(
    employees.c.name,
    salary_label,
).order_by("employee_salary")

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# LABEL - ORDER BY using the labeled expression directly.
# -------------------------------------------------------------------

salary_label = employees.c.salary.label("employee_salary")

stmt = select(
    employees.c.name,
    salary_label,
).order_by(salary_label.desc())

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# ALIAS + LABEL - Using table alias and column labels together.
# -------------------------------------------------------------------

employee = employees.alias("e")

stmt = select(
    employee.c.name.label("employee_name"),
    employee.c.salary.label("employee_salary"),
).order_by(employee.c.salary.desc())

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# SUBQUERY ALIAS - A subquery can be treated like a table.
# -------------------------------------------------------------------

high_salary_employees = (
    select(
        employees.c.id,
        employees.c.name,
        employees.c.salary,
    )
    .where(employees.c.salary > 60000)
    .subquery("high_salary")
)

stmt = select(
    high_salary_employees.c.name,
    high_salary_employees.c.salary,
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)


# -------------------------------------------------------------------
# ALIAS vs LABEL
#
# alias()  → Renames a table/query reference.
# label()  → Renames a column/expression in the result.
# -------------------------------------------------------------------

employee_alias = employees.alias("e")

stmt = select(
    employee_alias.c.name.label("employee_name"),
    employee_alias.c.salary.label("employee_salary"),
)

# Execute query
with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# Generated SQL
print(stmt)
