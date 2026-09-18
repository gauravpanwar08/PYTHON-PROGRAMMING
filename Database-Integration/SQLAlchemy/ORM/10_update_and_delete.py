# =====================================================================================
#                   SQLALCHEMY ORM — UPDATE + DELETE
#
# UPDATE modifies an existing database record.
# DELETE removes an existing database record.
#
# Important Methods:
#
# session.get(Model, primary_key) - Retrieve an ORM object using its primary key.
# session.commit()                - Flush pending changes and commit the transaction.
# session.update(obj)             - Update data into database
# session.delete(obj)             - Remove data from database
# session.dirty                   - Shows persistent objects that have been modified.
# session.deleted                 - Shows objects marked for deletion.
# ======================================================================================


from sqlalchemy import URL, String, create_engine
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
    __tablename__ = "orm_users_update_delete"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))


# Create table
Base.metadata.create_all(engine)


# Create Session factory
SessionLocal = sessionmaker(bind=engine)


# Insert sample data

with SessionLocal() as session:

    user1 = User(
        name="Gaurav",
        email="gaurav_update@example.com",
    )

    user2 = User(
        name="Rahul",
        email="rahul_delete@example.com",
    )

    session.add_all([user1, user2])
    session.commit()

    print("Sample users inserted.")


# ------------------------------------------------------------
# UPDATE - Retrieve object and modify its attribute
# ------------------------------------------------------------

with SessionLocal() as session:

    user = session.get(User, 1)

    if user:
        print("\nBefore UPDATE:")
        print(user.id, user.name, user.email)

        user.name = "Gaurav Panwar"

        print("\nModified object:")
        print(user.id, user.name, user.email)

        print("\nDirty objects:")
        print(session.dirty)

        session.commit()

        print("\nUser updated successfully!")


# ------------------------------------------------------------
# DELETE - Retrieve object and mark it for deletion
# ------------------------------------------------------------

with SessionLocal() as session:

    user = session.get(User, 2)

    if user:
        print("\nBefore DELETE:")
        print(user.id, user.name, user.email)

        session.delete(user)

        print("\nDeleted objects:")
        print(session.deleted)

        session.commit()

        print("\nUser deleted successfully!")


print("\nUPDATE + DELETE operation completed.")
