# ================================================================================
#                    SQLALCHEMY ORM — ORM EVENTS
#
# ORM Events allow us to automatically execute custom logic when specific
# ORM or Session lifecycle events occur.
#
# Important Events:
#
# before_insert  - Runs before an ORM INSERT during flush.
# after_insert   - Runs after an ORM INSERT during flush.
# before_update  - Runs before an ORM UPDATE during flush.
# after_update   - Runs after an ORM UPDATE during flush.
# before_delete  - Runs before an ORM DELETE during flush.
# after_delete   - Runs after an ORM DELETE during flush.
# before_flush   - Runs before the Session flushes pending changes.
# after_commit   - Runs after a transaction is committed.
# after_rollback  - Runs after a transaction is rolled back.
# set            - Runs when a mapped attribute is assigned a value.
#
# event.listens_for() - Registers an event listener for a specific event.
# ================================================================================


from sqlalchemy import URL, String, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


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


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "orm_event_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))


# ------------------------------------------------------------------------------
# before_insert - Runs before INSERT during flush.
# ------------------------------------------------------------------------------

@event.listens_for(User, "before_insert")
def before_insert(mapper, connection, target):
    target.name = target.name.strip().title()
    target.email = target.email.strip().lower()


# ------------------------------------------------------------------------------
# after_insert - Runs after INSERT during flush.
# ------------------------------------------------------------------------------

@event.listens_for(User, "after_insert")
def after_insert(mapper, connection, target):
    print(f"User inserted with ID: {target.id}")


# ------------------------------------------------------------------------------
# before_update - Runs before UPDATE during flush.
# ------------------------------------------------------------------------------

@event.listens_for(User, "before_update")
def before_update(mapper, connection, target):
    target.name = target.name.strip().title()
    target.email = target.email.strip().lower()


# ------------------------------------------------------------------------------
# before_delete - Runs before DELETE during flush.
# ------------------------------------------------------------------------------

@event.listens_for(User, "before_delete")
def before_delete(mapper, connection, target):
    print(f"Deleting user: {target.id}")


# ------------------------------------------------------------------------------
# Attribute set event - Runs when User.name is assigned a value.
# ------------------------------------------------------------------------------

@event.listens_for(User.name, "set")
def name_set(target, value, oldvalue, initiator):
    print(f"Name changed from {oldvalue} to {value}")


# ------------------------------------------------------------------------------
# Session before_flush - Runs before Session flushes pending changes.
# ------------------------------------------------------------------------------

@event.listens_for(Session, "before_flush")
def before_flush(session, flush_context, instances):
    print("Session is about to flush")


# ------------------------------------------------------------------------------
# Session after_commit - Runs after transaction commit.
# ------------------------------------------------------------------------------

@event.listens_for(Session, "after_commit")
def after_commit(session):
    print("Transaction committed")


# Create table
Base.metadata.create_all(engine)


with Session(engine) as session:

    # Create user
    user = User(
        name="  gaurav panwar  ",
        email="  GAURAV@EXAMPLE.COM  ",
    )

    session.add(user)

    # Flush triggers before_insert and after_insert
    session.flush()

    print(user.name)
    print(user.email)

    # Update user
    user.name = "  Gaurav Thakur  "

    session.flush()

    # Delete user
    session.delete(user)

    session.commit()
