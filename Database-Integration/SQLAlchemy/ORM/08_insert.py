# ==========================================================================================
#                SQLALCHEMY ORM — INSERT
#
# INSERT means adding new records into a database table.
# ORM INSERT : Python Object → Session → INSERT SQL → Database
#
# Important Methods:
# session.add(obj)              - Add one ORM object to the Session.
# session.add_all([obj1, obj2]) - Add multiple ORM objects to the Session.
# session.flush()               - Send pending changes to the database without committing.
# session.commit()              - Commit the current transaction permanently.
# session.new                   - Shows objects currently pending in the Session.
# ===========================================================================================


from sqlalchemy import URL, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

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
    __tablename__ = "orm_users_insert"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))


# Create table
Base.metadata.create_all(engine)


# ------------------------------------------------------------
# session.add() - Add one ORM object
# ------------------------------------------------------------

with Session(engine) as session:

    user = User(
        name="Gaurav",
        email="gaurav_insert_1@example.com",
    )

    session.add(user)

    print("Pending objects:", session.new)

    # Send INSERT to database without committing
    session.flush()

    print("Generated ID:", user.id)

    # Commit transaction
    session.commit()

    print("User inserted successfully!")


# ------------------------------------------------------------
# session.add_all() - Add multiple ORM objects
# ------------------------------------------------------------

with Session(engine) as session:

    user1 = User(
        name="Rahul",
        email="rahul_insert_1@example.com",
    )

    user2 = User(
        name="Aman",
        email="aman_insert_1@example.com",
    )

    session.add_all([user1, user2])

    session.commit()

    print("Multiple users inserted successfully!")


# Final Result

print("\nINSERT operation completed.")
