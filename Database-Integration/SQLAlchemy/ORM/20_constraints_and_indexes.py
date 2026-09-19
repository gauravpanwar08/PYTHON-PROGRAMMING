# ================================================================================
#                  SQLALCHEMY ORM — CONSTRAINTS & INDEXES
#
# Constraint → Ensure Data correctness and protect data  integrity.
#              Constraints define rules that control which data is allowed in the database.
#
# Index      → Improve Query/search performance.
#              Indexes improve the efficiency of searching and filtering database records.
#
# Important Constraints:
#
# primary_key       - Uniquely identifies each row.
# nullable          - Controls whether NULL values are allowed.
# unique            - Prevents duplicate values.
# ForeignKey        - Creates a database-level relationship between tables.
# CheckConstraint   - Enforces a custom condition.
# UniqueConstraint  - Enforces uniqueness across one or more columns.
#
# Important Index Concepts:
#
# index=True        - Creates an index for a mapped column.
# Index()           - Creates a single-column or multi-column index.
# __table_args__    - Defines table-level constraints and indexes.
# ================================================================================


from sqlalchemy import (
    URL,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
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
engine = create_engine(DATABASE_URL)


# ORM BASE

class Base(DeclarativeBase):
    pass


# ORM MODELS

class User(Base):
    __tablename__ = "orm_users_constraints"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    age: Mapped[int] = mapped_column(nullable=False)

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "age >= 18",
            name="ck_user_age_adult",
        ),
        UniqueConstraint(
            "name",
            "city",
            name="uq_user_name_city",
        ),
        Index(
            "ix_user_city_age",
            "city",
            "age",
        ),
    )

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "orm_addresses_constraints"

    id: Mapped[int] = mapped_column(primary_key=True)

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("orm_users_constraints.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="addresses")


# Create tables
Base.metadata.create_all(engine)


# ----------------------------------------------------------------------
# primary_key → Uniquely identifies each row.
# ----------------------------------------------------------------------

with Session(engine) as session:

    user = User(
        name="Gaurav",
        email="gaurav@example.com",
        age=25,
        city="Dehradun",
    )

    session.add(user)
    session.commit()

    print("User created:", user.id)


# ----------------------------------------------------------------------
# unique → Prevents duplicate values in a column.
# ----------------------------------------------------------------------

with Session(engine) as session:

    duplicate_user = User(
        name="Rahul",
        email="gaurav@example.com",
        age=24,
        city="Delhi",
    )

    session.add(duplicate_user)

    try:
        session.commit()

    except Exception as error:

        session.rollback()

        print("Unique constraint rejected duplicate email.")
        print(error)


# ----------------------------------------------------------------------
# nullable=False → Prevents NULL values.
# ----------------------------------------------------------------------

with Session(engine) as session:

    invalid_user = User(
        name=None,
        email="invalid@example.com",
        age=25,
        city="Delhi",
    )

    session.add(invalid_user)

    try:
        session.commit()

    except Exception as error:

        session.rollback()

        print("NOT NULL constraint rejected the data.")
        print(error)


# ----------------------------------------------------------------------
# CheckConstraint → Enforces a custom condition.
# ----------------------------------------------------------------------

with Session(engine) as session:

    invalid_user = User(
        name="Aman",
        email="aman@example.com",
        age=16,
        city="Mumbai",
    )

    session.add(invalid_user)

    try:
        session.commit()

    except Exception as error:

        session.rollback()

        print("CHECK constraint rejected the age.")
        print(error)


# ----------------------------------------------------------------------
# UniqueConstraint → Enforces uniqueness across multiple columns.
# ----------------------------------------------------------------------

with Session(engine) as session:

    user = User(
        name="Gaurav",
        email="gaurav2@example.com",
        age=26,
        city="Dehradun",
    )

    session.add(user)

    try:
        session.commit()

    except Exception as error:

        session.rollback()

        print("Composite unique constraint rejected the data.")
        print(error)


# ----------------------------------------------------------------------
# ForeignKey → Connects a child table to a parent table.
# ----------------------------------------------------------------------

with Session(engine) as session:

    user = session.scalar(
        select(User).where(User.email == "gaurav@example.com")
    )

    if user:

        address = Address(
            city="Dehradun",
            user_id=user.id,
        )

        session.add(address)
        session.commit()

        print("Address created for User:", user.id)
