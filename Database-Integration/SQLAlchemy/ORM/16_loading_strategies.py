# ================================================================================
#                    SQLALCHEMY ORM — LOADING STRATEGIES
#
# Loading strategies control when and how related ORM objects are loaded
# from the database.
#
# Lazy Loading → Related data is loaded only when the relationship is accessed.
# Eager Loading → Related data is loaded as part of the initial database operation.

# Important Loading Strategies Methods:
#
# select()        - Default loading- Loads related objects when the relationship is accessed.
# joinedload()    - Eagerly loads related objects using a JOIN.
# selectinload()  - Eagerly loads related objects using a SELECT IN query.
# raiseload()     - Prevents unexpected lazy loading and Raises an error if an unloaded relationship is accessed.
# options()       - Applies loading strategies to a SELECT statement.
# ================================================================================


from sqlalchemy import (
    URL,
    ForeignKey,
    String,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    joinedload,
    mapped_column,
    raiseload,
    relationship,
    selectinload,
    sessionmaker,
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


# DeclarativeBase


class Base(DeclarativeBase):
    pass


# ORM Models


class User(Base):
    __tablename__ = "orm_users_loading"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "orm_addresses_loading"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(ForeignKey("orm_users_loading.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")


# Create tables

Base.metadata.create_all(engine)


# Create Session factory

SessionLocal = sessionmaker(bind=engine)


# Insert sample data

with SessionLocal() as session:

    user1 = User(
        name="Gaurav",
        addresses=[
            Address(city="Dehradun"),
            Address(city="Delhi"),
        ],
    )

    user2 = User(
        name="Rahul",
        addresses=[
            Address(city="Mumbai"),
        ],
    )

    user3 = User(
        name="Aman",
        addresses=[],
    )

    session.add_all([user1, user2, user3])
    session.commit()


# ------------------------------------------------------------
# 1. LAZY LOADING - Default Relationship Behavior
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User)

    users = session.execute(stmt).scalars().all()

    print("\nLazy loading:")

    for user in users:

        print("\nUser:", user.name)

        # Relationship is loaded when accessed
        for address in user.addresses:
            print("Address:", address.city)


# ------------------------------------------------------------
# 2. JOINED LOADING - joinedload()
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).options(joinedload(User.addresses))

    result = session.execute(stmt)

    # unique() is required because joined eager loading of a collection
    # can produce multiple rows for the same User.
    users = result.unique().scalars().all()

    print("\nJoined loading:")

    for user in users:

        print("\nUser:", user.name)

        for address in user.addresses:
            print("Address:", address.city)


# ------------------------------------------------------------
# 3. SELECT-IN LOADING - selectinload()
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).options(selectinload(User.addresses))

    users = session.execute(stmt).scalars().all()

    print("\nSelect-in loading:")

    for user in users:

        print("\nUser:", user.name)

        for address in user.addresses:
            print("Address:", address.city)


# ------------------------------------------------------------
# 4. RAISING LAZY LOAD - raiseload()
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User).options(raiseload(User.addresses))

    users = session.execute(stmt).scalars().all()

    print("\nRaiseload:")

    for user in users:

        print("User:", user.name)

        try:
            print(user.addresses)

        except Exception as e:
            print("Relationship was not loaded:", type(e).__name__)


# ------------------------------------------------------------
# 5. JOIN vs joinedload()
# ------------------------------------------------------------

with SessionLocal() as session:

    # join() is used to JOIN tables in the SQL query.
    stmt = select(User).join(User.addresses).where(Address.city == "Delhi")

    users = session.execute(stmt).scalars().all()

    print("\nJOIN - Users having an address in Delhi:")

    for user in users:
        print(user.name)


with SessionLocal() as session:

    # joinedload() is used to load the relationship.
    stmt = select(User).options(joinedload(User.addresses))

    users = session.execute(stmt).unique().scalars().all()

    print("\njoinedload() - Users with loaded addresses:")

    for user in users:

        print("\nUser:", user.name)

        for address in user.addresses:
            print("Address:", address.city)


print("\nLoading strategies operation completed.")
