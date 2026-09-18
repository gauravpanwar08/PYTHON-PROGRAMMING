# ================================================================================
#               SQLALCHEMY ORM — SELECT
#
# SELECT is used to retrieve records from the database.
#
# Important Methods:
#
# select(User)          - Creates a SELECT statement for the ORM model.
# session.execute(stmt) - Executes the statement and returns a Result object.
# result.scalars()      - Extracts ORM objects from the result.
# scalars().all()       - Returns all ORM objects.
# scalars().first()     - Returns the first ORM object or None.
# scalars().one()       - Requires exactly one ORM object.
# session.get(Model, primary_key) - Retrieves an ORM object using its primary key.
# ===================================================================================


from sqlalchemy import URL, String, create_engine, select
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


# ------------------------------------------------------------
# DeclarativeBase
# ------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# ORM Model

class User(Base):
    __tablename__ = "orm_users_select"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))


# Create table
Base.metadata.create_all(engine)


# Create Session factory
SessionLocal = sessionmaker(bind=engine)


# Insert sample data

with SessionLocal() as session:

    users = [
        User(name="Gaurav", email="gaurav_select@example.com"),
        User(name="Rahul", email="rahul_select@example.com"),
        User(name="Aman", email="aman_select@example.com"),
    ]

    session.add_all(users)
    session.commit()


# ------------------------------------------------------------
# select(User) - Retrieve all users
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User)

    result = session.execute(stmt)

    users = result.scalars().all()

    print("\nAll Users:")

    for user in users:
        print(user.id, user.name, user.email)


# ------------------------------------------------------------
# scalars().first() - Retrieve the first user
# ------------------------------------------------------------

with SessionLocal() as session:

    stmt = select(User)

    user = session.execute(stmt).scalars().one()
    user = session.execute(stmt).scalars().first()

    print("\nFirst User:")

    if user:
        print(user.id, user.name, user.email)


# ------------------------------------------------------------
# session.get() - Retrieve user by primary key
# ------------------------------------------------------------

with SessionLocal() as session:

    user = session.get(User, 1)

    print("\nUser with ID 1:")

    if user:
        print(user.id, user.name, user.email)
    else:
        print("User not found")


print("\nSELECT operation completed.")
