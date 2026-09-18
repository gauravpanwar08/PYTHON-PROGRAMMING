# ============================================================
#                 SQLALCHEMY ORM — COMPLETE CRUD
#
# CRUD:
#
# C → CREATE → INSERT
# R → READ   → SELECT
# U → UPDATE → Modify
# D → DELETE → Remove
#
# Important Methods:
#
# session.add(obj)                - Add one ORM object
# session.add_all([...])          - Add multiple ORM objects
# select(Model)                   - Create a SELECT statement
# session.execute(stmt)           - Execute the statement
# result.scalars().all()          - Return all ORM objects
# session.get(Model, primary_key) - Retrieve an object by primary key
# session.commit()                - Commit the transaction
# session.update(obj)             - Update data into database
# session.delete(obj)             - Mark an ORM object for deletion
# ============================================================


from sqlalchemy import URL, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy.orm import mapped_column, sessionmaker

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
    __tablename__ = "orm_users_crud"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))


# Create table

Base.metadata.create_all(engine)


# Create Session factory

SessionLocal = sessionmaker(bind=engine)


# ------------------------------------------------------------
# CREATE - Insert users
# ------------------------------------------------------------

with SessionLocal() as session:

    user1 = User(
        name="Gaurav",
        email="gaurav_crud@example.com",
    )

    user2 = User(
        name="Rahul",
        email="rahul_crud@example.com",
    )

    session.add_all([user1, user2])

    session.commit()

    print("\nCREATE:")
    print("Users inserted successfully.")


# ------------------------------------------------------------
# READ - Select all users
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User)

    result = session.execute(stmt)

    users = result.scalars().all()

    print("\nREAD:")

    for user in users:
        print(user.id, user.name, user.email)


# ------------------------------------------------------------
# READ - Select one user by primary key
# ------------------------------------------------------------

with SessionLocal() as session:

    user = session.get(User, 1)

    print("\nREAD ONE:")

    if user:
        print(user.id, user.name, user.email)
    else:
        print("User not found.")


# ------------------------------------------------------------
# UPDATE - Modify an existing ORM object
# ------------------------------------------------------------

with SessionLocal() as session:

    user = session.get(User, 1)

    if user:

        print("\nBefore UPDATE:")
        print(user.id, user.name, user.email)

        user.name = "Gaurav Panwar"

        session.commit()

        print("\nAfter UPDATE:")
        print(user.id, user.name, user.email)

        print("User updated successfully.")


# ------------------------------------------------------------
# DELETE - Remove an ORM object
# ------------------------------------------------------------

with SessionLocal() as session:

    user = session.get(User, 2)

    if user:

        print("\nBefore DELETE:")
        print(user.id, user.name, user.email)

        session.delete(user)

        session.commit()

        print("User deleted successfully.")


# Verify remaining users

with SessionLocal() as session:

    stmt = select(User)

    users = session.execute(stmt).scalars().all()

    print("\nFINAL USERS:")

    for user in users:
        print(user.id, user.name, user.email)


print("\nComplete ORM CRUD operation finished.")
