# ===============================================================================================
#                  SQLALCHEMY ORM — N+1 QUERY Problem - Lazy Loading
#
# N+1 Query Problem occurs when one query loads the main records,
# and additional queries are executed for each related record.
# Goal : Avoid unnecessary database queries when accessing relationships.
#
# Example:
# 1 query  → Load Users
# N queries → Load Addresses for each User
# Total     → N + 1 queries
# This can cause serious performance problems when the number of records grows.
#
# Important Methods:
# select()        - Default loading- Loads related objects when the relationship is accessed.
# options()      - Applies ORM loading strategies to a SELECT statement.
# selectinload() - Loads related objects using a separate IN query.
# joinedload()   - Loads related objects using a SQL JOIN.
# unique()       - Removes duplicate ORM objects produced by joined eager loading.
# ===============================================================================================


from sqlalchemy import URL, create_engine, ForeignKey, String, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
    joinedload,
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


# ORM MODELS

class User(Base):
    __tablename__ = "orm_users_n_plus_one"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "orm_addresses_n_plus_one"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey("orm_users_n_plus_one.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")


# Create tables
Base.metadata.create_all(engine)


# SAMPLE DATA

with Session(engine) as session:

    # Add sample users
    user1 = User(name="Gaurav")
    user2 = User(name="Rahul")
    user3 = User(name="Aman")

    # Add addresses
    user1.addresses = [
        Address(city="Dehradun"),
        Address(city="Delhi"),
    ]

    user2.addresses = [
        Address(city="Mumbai"),
    ]

    # Aman has no address

    session.add_all([user1, user2, user3])
    session.commit()

# --------------------------------------------------
# 1. LAZY LOADING — N+1
# --------------------------------------------------

with Session(engine) as session:

    # Load all users
    stmt = select(User)
    users = session.scalars(stmt).all()

    # Access relationship inside loop
    for user in users:
        print(user.name)

        # This can trigger a separate query for each user
        for address in user.addresses:
            print("   ", address.city)


# -----------------------------------------------------------------------------------------------------
# 2. SELECTINLOAD — SOLVE N+1
#
# selectinload() loads all required related records using a separate SELECT query with an IN condition.
# ------------------------------------------------------------------------------------------------------

with Session(engine) as session:

    stmt = select(User).options(selectinload(User.addresses))

    users = session.scalars(stmt).all()

    # Addresses are already loaded
    for user in users:
        print(user.name)

        for address in user.addresses:
            print("   ", address.city)


# -----------------------------------------------------------------------------------------------------
# 3. JOINEDLOAD — SOLVE N+1
#
# joinedload() loads related records using a SQL JOIN.
# For collection relationships, unique() is required because one User can produce multiple result rows.
# -----------------------------------------------------------------------------------------------------

with Session(engine) as session:

    stmt = select(User).options(joinedload(User.addresses))

    result = session.execute(stmt)

    users = result.unique().scalars().all()

    for user in users:
        print(user.name)

        for address in user.addresses:
            print("   ", address.city)
