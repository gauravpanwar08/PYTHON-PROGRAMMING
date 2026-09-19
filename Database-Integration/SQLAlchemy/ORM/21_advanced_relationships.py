# ================================================================================================================================
#                    SQLALCHEMY ORM — ADVANCED RELATIONSHIPS
#
# Advanced relationships are used when a normal relationship configuration is not enough to describe the required ORM behavior.
#
# Important relationship() Parameters:
#
# primaryjoin   - Defines the primary join condition for a relationship.
#                 Custom relationship join condition.
# secondary     - Association table used for many-to-many relationships.
# secondaryjoin - Defines the join condition from the association table to the target table.
# foreign_keys  - Specifies which foreign key columns a relationship should use.
# remote_side   - Identifies the remote side of a self-referential relationship.
# viewonly      - Makes a relationship read-only from the ORM perspective.
# order_by      - Controls the ordering of related objects.
# overlaps      - Indicates that multiple relationships intentionally share overlapping foreign-key columns.
#                 Declares intentionally overlapping relationships.
#
# Advanced Patterns:
#
# Self-referential relationship
# Multiple foreign keys
# Explicit join conditions
# Filtered/read-only relationships
# Advanced many-to-many relationships
# ====================================================================================================================


from sqlalchemy import (
    URL,
    Column,
    ForeignKey,
    String,
    Table,
    and_,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    foreign,
    mapped_column,
    relationship,
)

# Create PostgreSQL connection URL
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="aura123",
    host="localhost",
    port=5432,
    database="sqlalchemy_db",
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


# ORM BASE

class Base(DeclarativeBase):
    pass


# ----------------------------------------------------------------------------------
# 1. SELF-REFERENTIAL RELATIONSHIP
#
# A model is related to another row of the same model.
# Example: Employee → Manager → Employee
# ----------------------------------------------------------------------------------


class Employee(Base):
    __tablename__ = "orm_employees_advanced"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("orm_employees_advanced.id")
    )

    manager: Mapped["Employee | None"] = relationship(
        "Employee",
        remote_side=[id],
        back_populates="employees",
    )

    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="manager",
    )


# ----------------------------------------------------------------------------------
# 2. MULTIPLE FOREIGN KEYS
#
# Multiple foreign keys can point to the same target table.
# ----------------------------------------------------------------------------------


class User(Base):
    __tablename__ = "orm_users_advanced"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


class Task(Base):
    __tablename__ = "orm_tasks_advanced"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_by_id: Mapped[int] = mapped_column(ForeignKey("orm_users_advanced.id"))

    approved_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("orm_users_advanced.id")
    )

    created_by: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by_id],
    )

    approved_by: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[approved_by_id],
    )


# ----------------------------------------------------------------------------------
# 3. MANY-TO-MANY WITH SECONDARY
#
# The association table connects two ORM models.
# ----------------------------------------------------------------------------------


user_course = Table(
    "orm_user_course_advanced",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("orm_users_advanced.id"),
        primary_key=True,
    ),
    Column(
        "course_id",
        ForeignKey("orm_courses_advanced.id"),
        primary_key=True,
    ),
)


class Course(Base):
    __tablename__ = "orm_courses_advanced"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_course,
        back_populates="courses",
    )


User.courses = relationship(
    "Course",
    secondary=user_course,
    back_populates="users",
)


# ----------------------------------------------------------------------------------
# 4. ORDER_BY
#
# Controls the order in which related objects are loaded.
# ----------------------------------------------------------------------------------


class Department(Base):
    __tablename__ = "orm_departments_advanced"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    employees: Mapped[list["DepartmentEmployee"]] = relationship(
        "DepartmentEmployee",
        back_populates="department",
        order_by="DepartmentEmployee.name",
    )


class DepartmentEmployee(Base):
    __tablename__ = "orm_department_employees_advanced"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("orm_departments_advanced.id")
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees",
    )


# ----------------------------------------------------------------------------------
# 5. PRIMARYJOIN
#
# primaryjoin allows an explicit relationship join condition.
# Here only addresses from Delhi are exposed through the relationship.
# ----------------------------------------------------------------------------------


class Customer(Base):
    __tablename__ = "orm_customers_advanced"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    addresses: Mapped[list["CustomerAddress"]] = relationship(
        "CustomerAddress",
        primaryjoin=lambda: and_(
            Customer.id == CustomerAddress.customer_id,
            CustomerAddress.city == "Delhi",
        ),
        viewonly=True,
    )


class CustomerAddress(Base):
    __tablename__ = "orm_customer_addresses_advanced"

    id: Mapped[int] = mapped_column(primary_key=True)

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(ForeignKey("orm_customers_advanced.id"))


# Create tables
Base.metadata.create_all(engine)


# ----------------------------------------------------------------------------------
# 6. SELF-REFERENTIAL RELATIONSHIP
# ----------------------------------------------------------------------------------

with Session(engine) as session:

    manager = Employee(name="Gaurav")

    employee1 = Employee(
        name="Rahul",
        manager=manager,
    )

    employee2 = Employee(
        name="Aman",
        manager=manager,
    )

    session.add_all(
        [
            manager,
            employee1,
            employee2,
        ]
    )

    session.commit()


with Session(engine) as session:

    manager = session.scalar(select(Employee).where(Employee.name == "Gaurav"))

    if manager:

        print("Manager:", manager.name)

        for employee in manager.employees:
            print("Employee:", employee.name)


# ----------------------------------------------------------------------------------
# 7. MULTIPLE FOREIGN KEYS RELATIONSHIP
# ----------------------------------------------------------------------------------

with Session(engine) as session:

    creator = User(name="Gaurav")
    approver = User(name="Rahul")

    session.add_all(
        [
            creator,
            approver,
        ]
    )

    session.flush()

    task = Task(
        title="Deploy API",
        created_by=creator.id,
        approved_by=approver.id,
    )

    session.add(task)
    session.commit()

    print("Task created:", task.title)


# ----------------------------------------------------------------------------------
# 8. MANY-TO-MANY RELATIONSHIP
# ----------------------------------------------------------------------------------

with Session(engine) as session:

    user = User(name="Aman")

    course1 = Course(title="Python Backend")
    course2 = Course(title="SQLAlchemy ORM")

    user.courses = [
        course1,
        course2,
    ]

    session.add(user)
    session.commit()

    print("Courses assigned to user.")


# ----------------------------------------------------------------------------------
# 9. ORDER_BY PRACTICAL
# ----------------------------------------------------------------------------------

with Session(engine) as session:

    department = Department(
        name="Backend",
        employees=[
            DepartmentEmployee(name="Zaid"),
            DepartmentEmployee(name="Aman"),
            DepartmentEmployee(name="Gaurav"),
        ],
    )

    session.add(department)
    session.commit()


with Session(engine) as session:

    department = session.scalar(select(Department).where(Department.name == "Backend"))

    if department:

        for employee in department.employees:
            print(employee.name)


# ----------------------------------------------------------------------------------
# 10. VIEWONLY + PRIMARYJOIN PRACTICAL
# ----------------------------------------------------------------------------------

with Session(engine) as session:

    customer = Customer(
        name="Gaurav",
    )

    session.add(customer)
    session.flush()

    session.add_all(
        [
            CustomerAddress(
                city="Delhi",
                customer_id=customer.id,
            ),
            CustomerAddress(
                city="Mumbai",
                customer_id=customer.id,
            ),
        ]
    )

    session.commit()


with Session(engine) as session:

    customer = session.scalar(select(Customer).where(Customer.name == "Gaurav"))

    if customer:

        print("Delhi addresses:")

        for address in customer.addresses:
            print(address.city)
