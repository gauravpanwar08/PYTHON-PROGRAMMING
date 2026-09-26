from sqlalchemy import select

from database import engine
from tables import employees

# ---------------- Search + Filtering ----------------

def search_employees(name):
    with engine.connect() as connection:
        result = connection.execute(
            select(
                employees.c.id,
                employees.c.name,
                employees.c.email,
                employees.c.age
            ).where(
                employees.c.name.like(f"%{name}%")
            )
        )
        return result.all()
    
print(search_employees("Gau"))



# ---------------- Sorting + Pagination ----------------

def get_employees_sorted():
    with engine.connect() as connection:
        result = connection.execute(
            select(employees).order_by(employees.c.age.desc())
        )
        return result.all()


def get_employees_paginated(page, page_size):
    offset = (page - 1) * page_size

    with engine.connect() as connection:
        result = connection.execute(
            select(employees)
            .offset(offset)
            .limit(page_size)
        )
        return result.all()

print(get_employees_sorted())
print(get_employees_paginated(1, 3))


# ---------------- Aggregate Reports ----------------

from sqlalchemy import select, func

from database import engine
from tables import employees, departments


def get_employee_count():
    with engine.connect() as connection:
        result = connection.execute(
            select(func.count(employees.c.id))
        )
        return result.scalar()


def get_average_age():
    with engine.connect() as connection:
        result = connection.execute(
            select(func.avg(employees.c.age))
        )
        return result.scalar()


def get_employee_count_by_department():
    with engine.connect() as connection:
        result = connection.execute(
            select(
                departments.c.name,
                func.count(employees.c.id)
            )
            .select_from(
                departments.outerjoin(
                    employees,
                    departments.c.id == employees.c.department_id
                )
            )
            .group_by(departments.c.id)
        )
        return result.all()

# ---------------------- CTE Report -----------------------

from sqlalchemy import select, func

from database import engine
from tables import employees, departments


def department_employee_report():
    employee_counts = (
        select(
            employees.c.department_id,
            func.count(employees.c.id).label("employee_count")
        )
        .group_by(employees.c.department_id)
        .cte("employee_counts")
    )

    with engine.connect() as connection:
        result = connection.execute(
            select(
                departments.c.name,
                employee_counts.c.employee_count
            )
            .select_from(
                departments.join(
                    employee_counts,
                    departments.c.id == employee_counts.c.department_id
                )
            )
        )
        return result.all()


# --------------------- Window Function Report -----------------------

from sqlalchemy import select, func

from database import engine
from tables import employees


def employee_age_rank():
    age_rank = func.row_number().over(
        order_by=employees.c.age.desc()
    ).label("age_rank")

    with engine.connect() as connection:
        result = connection.execute(
            select(
                employees.c.name,
                employees.c.age,
                age_rank
            )
        )
        return result.all()
