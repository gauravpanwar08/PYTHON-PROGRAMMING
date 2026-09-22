# ================================================================================
#                    SQLALCHEMY ORM — PERFORMANCE % OPTIMIZATION
#
# ORM performance means reducing unnecessary database queries, unnecessary data loading, 
# Python-side processing, and excessive ORM object creation.
#
# Important Concepts:
#
# N+1 Query          - One query for parent rows + N queries for relationships.
# selectinload()     - Efficiently loads collections using a separate IN query.
# joinedload()       - Loads relationships using JOIN.
# Column Selection   - Loads only the columns actually required.
# Database Filtering - Lets the database filter rows instead of Python.
# Pagination         - Limits the number of rows returned per request.
# Indexes            - Help the database find rows efficiently.
# EXPLAIN ANALYZE    - PostgreSQL tool for inspecting query execution.
# Bulk Operations    - Efficient for large/simple data operations.
# Session Lifecycle  - Avoids unnecessarily long-lived ORM sessions.
# Streaming          - Processes large result sets without loading everything into memory at once.
# ================================================================================


from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    joinedload,
    mapped_column,
    relationship,
    selectinload,
    sessionmaker,
)


# Create engine
engine = create_engine(
    "postgresql+psycopg://postgres:aura123@localhost:5432/sqlalchemy_db",
    echo=True,
)


# Create Declarative Base
class Base(DeclarativeBase):
    pass


# Create User model
class User(Base):
    __tablename__ = "performance_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    age: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user"
    )

    __table_args__ = (
        Index("ix_performance_users_age", "age"),
    )


# Create Order model
class Order(Base):
    __tablename__ = "performance_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("performance_users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="orders"
    )


# Create tables
Base.metadata.create_all(engine)

# Create Session factory
SessionLocal = sessionmaker(bind=engine)


with SessionLocal() as session:

    # Insert sample data
    user1 = User(
        name="Gaurav",
        email="gaurav_performance@example.com",
        age=22,
        orders=[
            Order(product="Laptop", amount=70000),
            Order(product="Keyboard", amount=3000),
        ],
    )

    user2 = User(
        name="Rahul",
        email="rahul_performance@example.com",
        age=24,
        orders=[
            Order(product="Mouse", amount=1500),
        ],
    )

    user3 = User(
        name="Aman",
        email="aman_performance@example.com",
        age=17,
        orders=[],
    )

    session.add_all([user1, user2, user3])
    session.commit()


    # ----------------------------------------------------------------
    # N+1 Query Problem - Loads users first and then queries orders separately for each user.
    # ----------------------------------------------------------------

    users = session.scalars(
        select(User)
    ).all()

    for user in users:
        print(user.name, user.orders)


    # ----------------------------------------------------------------
    # selectinload() - Avoids N+1 by loading all orders with a
    # separate IN query.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .options(selectinload(User.orders))
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name, user.orders)


    # ----------------------------------------------------------------
    # joinedload() - Loads users and orders using JOIN.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .options(joinedload(User.orders))
    )

    result = session.execute(stmt)

    # unique() is required for collection joinedload().
    users = result.unique().scalars().all()

    for user in users:
        print(user.name, user.orders)


    # ----------------------------------------------------------------
    # Selecting only required columns - Avoid loading complete ORM
    # objects when only specific fields are needed.
    # ----------------------------------------------------------------

    stmt = select(
        User.id,
        User.name,
    )

    rows = session.execute(stmt).all()

    for row in rows:
        print(row.id, row.name)


    # ----------------------------------------------------------------
    # Database-side filtering - Let PostgreSQL filter rows instead
    # of loading everything and filtering in Python.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .where(
            User.is_active.is_(True),
            User.age >= 18,
        )
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name)


    # ----------------------------------------------------------------
    # Pagination - Load only a limited number of rows.
    # ----------------------------------------------------------------

    page = 1
    page_size = 2

    stmt = (
        select(User)
        .order_by(User.id)
        .limit(page_size)
        .offset((page - 1) * page_size)
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.id, user.name)


    # ----------------------------------------------------------------
    # Counting rows - Ask the database for the count instead of loading all ORM objects.
    # ----------------------------------------------------------------

    stmt = select(
        func.count(User.id)
    )

    total_users = session.scalar(stmt)

    print("Total users:", total_users)


    # ----------------------------------------------------------------
    # Index - The User.age column has an index defined in __table_args__.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .where(User.age == 22)
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name)


    # ----------------------------------------------------------------
    # Avoid unnecessary relationship loading - If the endpoint only
    # needs user information, don't load orders.
    # ----------------------------------------------------------------

    stmt = select(User)

    users = session.scalars(stmt).all()

    for user in users:
        print(user.id, user.name)


    # ----------------------------------------------------------------
    # Aggregate in the database - Calculate totals in PostgreSQL
    # instead of loading every order into Python.
    # ----------------------------------------------------------------

    stmt = select(
        func.sum(Order.amount)
    )

    total_sales = session.scalar(stmt)

    print("Total sales:", total_sales)


    # ----------------------------------------------------------------
    # Streaming large result sets - Process rows incrementally
    # instead of immediately creating a large Python list.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .execution_options(yield_per=100)
    )

    result = session.scalars(stmt)

    for user in result:
        print(user.id, user.name)


    # ----------------------------------------------------------------
    # Bulk-style operation - Useful when a large/simple operation
    # does not require normal ORM object-by-object processing.
    # ----------------------------------------------------------------

    session.execute(
        User.__table__.update()
        .where(User.age < 18)
        .values(age=18)
    )

    session.commit()


# ----------------------------------------------------------------
# PostgreSQL EXPLAIN ANALYZE
#
# Run the generated SQL/query directly in PostgreSQL when you want
# to inspect the actual execution plan.
#
# Example:
#
# EXPLAIN ANALYZE
# SELECT *
# FROM performance_users
# WHERE age = 22;
# ----------------------------------------------------------------
