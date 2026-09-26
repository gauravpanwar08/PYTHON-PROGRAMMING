from sqlalchemy import Table, Column, String, Integer, ForeignKey, CheckConstraint
from database import metadata

# create departments table

departments = Table(
    "departments",
    metadata,    
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False, unique=True)
)

# create employees table

employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("age", Integer, nullable=False),
    CheckConstraint("age >= 18", name="ck_employees_age"),
    Column("department_id", Integer, ForeignKey("departments.id"))
)

# create projects table

projects = Table(
    "projects",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("department_id", Integer, ForeignKey("departments.id"))
)

# create employee_projects table

employee_projects = Table(
    "employee_projects",
    metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True)
)
