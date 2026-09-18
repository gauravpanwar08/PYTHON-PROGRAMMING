# ================================================================================
#                    SQLALCHEMY ORM — AGGREGATIONS
#
# Aggregation means calculating a single value from multiple records.
#
# Common aggregate functions:
#
# count()      - Counts rows or values.
# sum()        - Calculates the total of numeric values.
# avg()        - Calculates the average of numeric values.
# min()        - Returns the minimum value.
# max()        - Returns the maximum value.
#
# Important Methods:
#
# group_by()   - Groups rows with the same value for aggregation.
# having()     - Filters grouped results after aggregation/grouping.
# where()      - Filters individual rows before aggregation/grouping.
# scalar()     - Returns the first column of the first result row.
# scalars()    - Extracts the first column from all result rows.
# ================================================================================


from sqlalchemy import URL, String, create_engine, func, select
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
    __tablename__ = "orm_users_aggregations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int]
    city: Mapped[str] = mapped_column(String(100))


# Create table

Base.metadata.create_all(engine)


# Create Session factory

SessionLocal = sessionmaker(bind=engine)


# Insert sample data

with SessionLocal() as session:

    users = [
        User(name="Gaurav", age=22, city="Dehradun"),
        User(name="Rahul", age=17, city="Delhi"),
        User(name="Aman", age=25, city="Mumbai"),
        User(name="Gauri", age=21, city="Delhi"),
        User(name="Rohit", age=30, city="Dehradun"),
        User(name="Neha", age=24, city="Mumbai"),
    ]

    session.add_all(users)
    session.commit()


# ------------------------------------------------------------
# COUNT - Count total number of users
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(func.count(User.id))
    count = session.execute(stmt).scalar()

    print("\nTotal users:")
    print(count)


# ------------------------------------------------------------
# SUM - Calculate total age
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(func.sum(User.age))
    total_age = session.execute(stmt).scalar()

    print("\nTotal age:")
    print(total_age)


# ------------------------------------------------------------
# AVG - Calculate average age
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(func.avg(User.age))
    average_age = session.execute(stmt).scalar()

    print("\nAverage age:")
    print(average_age)


# ------------------------------------------------------------
# MIN - Find minimum age
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(func.min(User.age))
    minimum_age = session.execute(stmt).scalar()

    print("\nMinimum age:")
    print(minimum_age)


# ------------------------------------------------------------
# MAX - Find maximum age
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(func.max(User.age))
    maximum_age = session.execute(stmt).scalar()

    print("\nMaximum age:")
    print(maximum_age)


# ------------------------------------------------------------
# WHERE + COUNT : Count users older than 18
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(func.count(User.id)).where(User.age >= 18)
    count = session.execute(stmt).scalar()

    print("\nUsers age >= 18:")
    print(count)


# ------------------------------------------------------------
# GROUP BY - Count users in each city
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(
        User.city,
        func.count(User.id),
    ).group_by(User.city)

    result = session.execute(stmt)

    print("\nUsers per city:")

    for city, count in result:
        print(city, count)


# ------------------------------------------------------------
# GROUP BY + AVG : Average age per city
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(
        User.city,
        func.avg(User.age),
    ).group_by(User.city)

    result = session.execute(stmt)

    print("\nAverage age per city:")

    for city, average_age in result:
        print(city, average_age)


# ------------------------------------------------------------
# HAVING - Cities with more than one user
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = (
        select(
            User.city,
            func.count(User.id),
        )
        .group_by(User.city)
        .having(func.count(User.id) > 1)
    )

    result = session.execute(stmt)

    print("\nCities with more than one user:")

    for city, count in result:
        print(city, count)


# ------------------------------------------------------------
# WHERE + GROUP BY + HAVING
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = (
        select(
            User.city,
            func.count(User.id),
        )
        .where(User.age >= 18)
        .group_by(User.city)
        .having(func.count(User.id) >= 2)
    )

    result = session.execute(stmt)

    print("\nCities with at least 2 adult users:")

    for city, count in result:
        print(city, count)


print("\nAggregation operation completed.")
