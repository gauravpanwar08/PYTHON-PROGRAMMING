# ================================================================================
#                    SQLALCHEMY ORM — FILTERING
#
# Filtering means retrieving only the records that satisfy a specific condition.
# Basic pattern: select(model).where(condition)
# where() - Adds filtering conditions to a SELECT statement.
# Comparison operators: ==, !=, >, >=, <, <=
#
# Important Methods:
#
# and_()       - Requires all conditions to be true
# or_()        - Requires at least one condition to be true.
# not_()       - Negates a condition
# in_()        - Checks whether a value exists in a list
# not_in()     - Excludes values from a list
# like()       - Case-sensitive pattern matching
# ilike()      - Case-insensitive pattern matching
# is_(None)    - Checks for SQL NULL
# is_not(None) - Checks for SQL NOT NULL
# ====================================================================================


from sqlalchemy import URL, String, and_, create_engine, or_, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.orm import sessionmaker

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


# DeclarativeBase


class Base(DeclarativeBase):
    pass


# ORM Model


class User(Base):
    __tablename__ = "orm_users_filtering"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))
    age: Mapped[int]
    city: Mapped[str] = mapped_column(String(100))


# Create table
Base.metadata.create_all(engine)


# Create Session factory
SessionLocal = sessionmaker(bind=engine)


# Insert sample data

with SessionLocal() as session:

    users = [
        User(
            name="Gaurav",
            email="gaurav_filter@example.com",
            age=22,
            city="Dehradun",
        ),
        User(
            name="Rahul",
            email="rahul@example.com",
            age=17,
            city="Delhi",
        ),
        User(
            name="Aman",
            email="aman@example.com",
            age=25,
            city="Mumbai",
        ),
        User(
            name="Gauri",
            email="gauri@example.com",
            age=21,
            city="Delhi",
        ),
    ]

    session.add_all(users)
    session.commit()


# ------------------------------------------------------------
# Basic filtering - Users with age greater than 18
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).where(User.age > 18)

    users = session.execute(stmt).scalars().all()

    print("\nAge > 18:")

    for user in users:
        print(user.name, user.age)


# ------------------------------------------------------------
# AND condition - Age >= 18 AND city = Delhi
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).where(
        and_(
            User.age >= 18,
            User.city == "Delhi",
        )
    )

    users = session.execute(stmt).scalars().all()

    print("\nAge >= 18 AND Delhi:")

    for user in users:
        print(user.name, user.age, user.city)


# ------------------------------------------------------------
# OR condition - City = Delhi OR Dehradun
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).where(
        or_(
            User.city == "Delhi",
            User.city == "Dehradun",
        )
    )

    users = session.execute(stmt).scalars().all()

    print("\nDelhi OR Dehradun:")

    for user in users:
        print(user.name, user.city)


# ------------------------------------------------------------
# IN condition - Users from selected cities
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).where(User.city.in_(["Delhi", "Mumbai"]))

    users = session.execute(stmt).scalars().all()

    print("\nCity IN Delhi/Mumbai:")

    for user in users:
        print(user.name, user.city)


# ------------------------------------------------------------
# LIKE condition - Names starting with G
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).where(User.name.like("G%"))

    users = session.execute(stmt).scalars().all()

    print("\nNames starting with G:")

    for user in users:
        print(user.name)


# ------------------------------------------------------------
# ILIKE condition - Case-insensitive search
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).where(User.name.ilike("gaur%"))

    users = session.execute(stmt).scalars().all()

    print("\nCase-insensitive name search:")

    for user in users:
        print(user.name)


print("\nFiltering operation completed.")
