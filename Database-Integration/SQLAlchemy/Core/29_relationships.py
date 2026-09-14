# ============================================================================================================
#                               RELATIONSHIPS
#
# ForeignKey                    : Links a column to a primary/unique key of another table.
# ForeignKeyConstraint          : Defines a foreign key constraint for one or more columns.
# One-to-Many relationship      : One parent record can be related to many child records.
# Many-to-Many relationship     : Many records in one table can be related to many records in another table.
# Self-referential relationship : A table creates a relationship with itself.
# JOIN using Foreign Key        : Combines related tables using their foreign key relationship.
#
# Actions :
#     - ondelete="CASCADE"      : Automatically deletes related child records when the parent is deleted.
#     - ondelete="SET NULL"     : Set the foreign key to NULL when the parent is deleted.
#     - ondelete="RESTRICT"     : Prevent deleting the parent if related child records exist.
#     - ondelete="NO ACTION"    : Allow the database to enforce its normal foreign key behavior.
# ============================================================================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    ForeignKeyConstraint,
    select,
)


# Create engine
engine = create_engine("sqlite:///relationships.db", echo=True)

# Create metadata
metadata = MetaData()


# -------------------------------------------------------------------
# DEPARTMENTS TABLE
# -------------------------------------------------------------------

departments = Table(
    "departments",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
)


# -------------------------------------------------------------------
# EMPLOYEES TABLE — ONE-TO-MANY
# -------------------------------------------------------------------

employees = Table(
    "employees",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),

    Column(
        "department_id",
        Integer,
        ForeignKey(
            "departments.id",
            ondelete="CASCADE",
        ),
    ),
)


# -------------------------------------------------------------------
# STUDENTS TABLE
# -------------------------------------------------------------------

students = Table(
    "students",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
)


# -------------------------------------------------------------------
# COURSES TABLE
# -------------------------------------------------------------------

courses = Table(
    "courses",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
)


# -------------------------------------------------------------------
# STUDENT-COURSES — MANY-TO-MANY
# -------------------------------------------------------------------

student_courses = Table(
    "student_courses",
    metadata,

    Column("student_id", Integer, primary_key=True),
    Column("course_id", Integer, primary_key=True),

    ForeignKeyConstraint(
        ["student_id"],
        ["students.id"],
        name="fk_student_courses_student",
    ),

    ForeignKeyConstraint(
        ["course_id"],
        ["courses.id"],
        name="fk_student_courses_course",
    ),
)


# -------------------------------------------------------------------
# EMPLOYEE MANAGERS — SELF-REFERENTIAL
# -------------------------------------------------------------------

employee_managers = Table(
    "employee_managers",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),

    Column(
        "manager_id",
        Integer,
        ForeignKey("employee_managers.id"),
    ),
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
            {"id": 1, "name": "Gaurav", "department_id": 1},
            {"id": 2, "name": "Priya", "department_id": 1},
            {"id": 3, "name": "Rahul", "department_id": 2},
        ],
    )

    connection.execute(
        students.insert(),
        [
            {"id": 1, "name": "Aman"},
            {"id": 2, "name": "Neha"},
        ],
    )

    connection.execute(
        courses.insert(),
        [
            {"id": 1, "name": "Python"},
            {"id": 2, "name": "SQL"},
        ],
    )

    connection.execute(
        student_courses.insert(),
        [
            {"student_id": 1, "course_id": 1},
            {"student_id": 1, "course_id": 2},
            {"student_id": 2, "course_id": 1},
        ],
    )

    connection.execute(
        employee_managers.insert(),
        [
            {"id": 1, "name": "Gaurav", "manager_id": None},
            {"id": 2, "name": "Priya", "manager_id": 1},
            {"id": 3, "name": "Rahul", "manager_id": 2},
        ],
    )


# -------------------------------------------------------------------
# ONE-TO-MANY JOIN
# -------------------------------------------------------------------

stmt = (
    select(
        employees.c.name.label("employee"),
        departments.c.name.label("department"),
    )
    .join(departments)
)

with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# -------------------------------------------------------------------
# MANY-TO-MANY JOIN
# -------------------------------------------------------------------

stmt = (
    select(
        students.c.name.label("student"),
        courses.c.name.label("course"),
    )
    .join(
        student_courses,
        students.c.id == student_courses.c.student_id,
    )
    .join(
        courses,
        student_courses.c.course_id == courses.c.id,
    )
)

with engine.connect() as connection:
    result = connection.execute(stmt)

    for row in result:
        print(row)


# -------------------------------------------------------------------
# GENERATED SQL
# -------------------------------------------------------------------

print(
    stmt.compile(
        engine,
        compile_kwargs={"literal_binds": True},
    )
)