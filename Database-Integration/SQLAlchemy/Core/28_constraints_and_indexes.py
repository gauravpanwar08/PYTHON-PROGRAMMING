# =========================================================================================
#                             CONSTRAINTS & INDEXES
#
#   CONSTRAINTS : Rules that enforce data integrity and validity in a table.
#   INDEXES     : Data structures that speed up searching and querying table data.
#
# PrimaryKeyConstraint        : Ensures one or more columns uniquely identify each row.
# ForeignKeyConstraint        : Ensures values reference valid keys in another table.
# UniqueConstraint            : Ensures column values are unique across rows.
# CheckConstraint             : Ensures values satisfy a specified condition.
# Index                       : Speeds up data retrieval for one or more columns.
# Single-column index         : An index created on a single column.
# Composite index             : An index created on multiple columns.
# Constraint and index naming : Gives constraints and indexes explicit, predictable names.
# ===========================================================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
    CheckConstraint,
    Index,
)


# Create engine
engine = create_engine("sqlite:///constraints_and_indexes.db", echo=True)

# Create metadata
metadata = MetaData()


# -------------------------------------------------------------------
# DEPARTMENTS TABLE
# -------------------------------------------------------------------

departments = Table(
    "departments",
    metadata,

    Column("id", Integer),
    Column("name", String(50), nullable=False),

    PrimaryKeyConstraint("id", name="pk_departments"),
    UniqueConstraint("name", name="uq_departments_name"),
)


# -------------------------------------------------------------------
# EMPLOYEES TABLE
# -------------------------------------------------------------------

employees = Table(
    "employees",
    metadata,

    Column("id", Integer),
    Column("name", String(50), nullable=False),
    Column("email", String(100), nullable=False),
    Column("age", Integer, nullable=False),
    Column("department_id", Integer, nullable=False),

    PrimaryKeyConstraint("id", name="pk_employees"),

    UniqueConstraint(
        "email",
        name="uq_employees_email",
    ),

    CheckConstraint(
        "age >= 18",
        name="ck_employees_age",
    ),

    ForeignKeyConstraint(
        ["department_id"],
        ["departments.id"],
        name="fk_employees_department",
    ),
)


# -------------------------------------------------------------------
# INDEXES
# -------------------------------------------------------------------

# Single-column index
Index(
    "ix_employees_name",
    employees.c.name,
)

# Composite index
Index(
    "ix_employees_name_age",
    employees.c.name,
    employees.c.age,
)


# Create tables
metadata.create_all(engine)


# -------------------------------------------------------------------
# INSERT SAMPLE DATA
# -------------------------------------------------------------------

with engine.begin() as connection:

    connection.execute(
        departments.insert(),
        [
            {"id": 1, "name": "IT"},
            {"id": 2, "name": "HR"},
        ],
    )

    connection.execute(
        employees.insert(),
        [
            {
                "id": 1,
                "name": "Gaurav",
                "email": "gaurav@example.com",
                "age": 22,
                "department_id": 1,
            },
            {
                "id": 2,
                "name": "Priya",
                "email": "priya@example.com",
                "age": 24,
                "department_id": 2,
            },
        ],
    )


# -------------------------------------------------------------------
# GENERATED SQL
# -------------------------------------------------------------------

print(
    employees.insert().compile(
        engine,
        compile_kwargs={"literal_binds": True},
    )
)