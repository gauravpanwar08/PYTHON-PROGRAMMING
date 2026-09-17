# ===============================================================================================================
#                                  SESSION
#
# Session        : ORM workspace that manages ORM objects and database transactions.
#
# add()          : Adds one ORM object to the Session for tracking.
# add_all()      : Adds multiple ORM objects to the Session.
# commit()       : Commits the current transaction.
# rollback()     : Rolls back the current uncommitted transaction.
# flush()        : Sends pending changes to the database without committing the transaction.
# refresh()      : Refreshes an ORM object with the current database state.
# get()          : Retrieves an ORM object using its primary key.
# delete()       : Marks an ORM object for deletion.
# close()        : Closes the Session.
# session.new    : Returns a set of new ORM objects currently added to the Session.

# Session vs Engine:
# Engine         → Database connectivity and communication infrastructure.
# Session        → ORM object tracking and transaction management.
# ===============================================================================================================


from sqlalchemy import URL, create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# Database configuration

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="aura123",
    host="localhost",
    port=5432,
    database="sqlalchemy_db",
)


# Create engine

engine = create_engine(
    DATABASE_URL,
    echo=True
)


# -------------------------------------------------------------------
# DeclarativeBase - Base class used for SQLAlchemy ORM models.
# -------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# User model

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )


# Create table

Base.metadata.create_all(engine)


# -------------------------------------------------------------------
# Session - Manages ORM objects and database transactions.
# -------------------------------------------------------------------

with Session(engine) as session:

    # Create ORM object

    user = User(
        name="Gaurav",
        email="gaurav_session@gmail.com"
    )

    # -------------------------------------------------------------------
    # add() - Adds an ORM object to the Session for tracking.
    # -------------------------------------------------------------------

    session.add(user)

    print("Before commit:")
    print("User ID:", user.id)

    # -------------------------------------------------------------------
    # flush() - Sends pending changes to the database without committing.
    # -------------------------------------------------------------------

    session.flush()

    print("\nAfter flush:")
    print("User ID:", user.id)

    # -------------------------------------------------------------------
    # commit() - Commits the current transaction.
    # -------------------------------------------------------------------

    session.commit()

    print("\nAfter commit:")
    print("User ID:", user.id)
    print("User Name:", user.name)
    print("User Email:", user.email)
