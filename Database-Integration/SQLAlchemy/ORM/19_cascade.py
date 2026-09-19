# =====================================================================================================
#                         SQLALCHEMY ORM — CASCADE
#
# Cascade controls how ORM operations on a parent object are propagated to its related child objects.
#
# Important Cascade Options:
#
# save-update    - Related objects participate when parent is added to Session.
# merge          - Propagates merge operations to related objects.
# delete         - Deletes related objects when the parent is deleted.
# delete-orphan  - Deletes a child when it is removed/unlink from its parent collection.
# all            - Includes the commonly used cascade operations.
#
# Important relationship() Parameters:
#
# cascade        - Controls propagation of ORM operations to related objects.
# back_populates - Explicitly links relationships on both sides.
# ForeignKey     → Defines the database-level relationship.
# relationship() → Defines the ORM-level relationship.
# ================================================================================


from sqlalchemy import URL, ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
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
    __tablename__ = "orm_users_cascade"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Address(Base):
    __tablename__ = "orm_addresses_cascade"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(ForeignKey("orm_users_cascade.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")


# Create tables
Base.metadata.create_all(engine)


#   CREATE DATA
with Session(engine) as session:

    # Create user
    user = User(name="Gaurav")

    # Create related addresses
    user.addresses = [
        Address(city="Dehradun"),
        Address(city="Delhi"),
    ]

    # Add only the parent
    session.add(user)

    # Because of save-update cascade,
    # related Address objects also become part of the Session.
    session.commit()

    print("User and addresses created.")


# --------------------------------------------------------------------------------------
# DELETE CASCADE
#
# delete cascade means deleting the parent also deletes its related child objects.
# --------------------------------------------------------------------------------------

with Session(engine) as session:

    user = session.scalar(select(User).where(User.name == "Gaurav"))

    if user:
        # Delete parent
        session.delete(user)

        # Because of delete cascade,
        # related addresses are also marked for deletion.
        session.commit()

        print("User and related addresses deleted.")


# --------------------------------------------------------------------------------------
# DELETE-ORPHAN
#
# delete-orphan deletes a child when it is removed from the parent's relationship collection.
# --------------------------------------------------------------------------------------

with Session(engine) as session:

    # Create a new user
    user = User(name="Rahul")

    user.addresses = [
        Address(city="Mumbai"),
        Address(city="Pune"),
    ]

    session.add(user)
    session.commit()


with Session(engine) as session:

    user = session.scalar(select(User).where(User.name == "Rahul"))

    if user:

        # Remove one address from the parent collection
        address = user.addresses[0]

        user.addresses.remove(address)

        # Because of delete-orphan,
        # the removed Address is deleted from the database.
        session.commit()

        print("Orphaned address deleted.")

# --------------------------------------------------------------------------------------
# SAVE-UPDATE
#
# save-update allows related objects to participate in the Session when the parent object is added.
# --------------------------------------------------------------------------------------

with Session(engine) as session:

    user = User(name="Aman")

    address = Address(city="Dehradun")

    # Associate child with parent
    user.addresses.append(address)

    # Add only parent
    session.add(user)

    # Address is also persisted because of save-update.
    session.commit()

    print("User and address saved.")
