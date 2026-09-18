# =============================================================================================================
#                                  JOINS
#
# Core uses Table/Column objects vs ORM uses Model attributes and relationships.
#
# JOIN                    → Combines rows from multiple tables based on a related condition.
# join()                  → Performs an INNER JOIN in an ORM SELECT statement.
# outerjoin()             → Performs a LEFT OUTER JOIN and keeps unmatched rows from the left table.
# relationship-based JOIN → Uses an ORM relationship to determine the JOIN condition.
# join(Model)             → Joins directly to the target ORM model using available foreign-key relationships.
# JOIN + WHERE            → Joins related tables and filters the result.
# joinedload()            → Loads related ORM objects using a JOIN-based loading strategy.
#                           (Detailed later in Loading Strategies.)
# =============================================================================================================

from sqlalchemy import URL, String, ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

# Create database URL
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


# Create Declarative Base
class Base(DeclarativeBase):
    pass


# USER MODEL

class User(Base):
    __tablename__ = "orm_users_joins"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


# ADDRESS MODEL

class Address(Base):
    __tablename__ = "orm_addresses_joins"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))

    user_id: Mapped[int] = mapped_column(ForeignKey("orm_users_joins.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")


# Create tables
Base.metadata.create_all(engine)


# INSERT SAMPLE DATA
with Session(engine) as session:


    user1 = User(name="Gaurav")
    user1.addresses = [
        Address(city="Delhi"),
        Address(city="Dehradun"),
    ]

    user2 = User(name="Rahul")
    user2.addresses = [
        Address(city="Mumbai"),
    ]

    user3 = User(name="Aman")

    session.add_all([user1, user2, user3])
    session.commit()

    # ------------------------------------------------------------------------------
    # 1. INNER JOIN - Returns users that have matching addresses.
    # ------------------------------------------------------------------------------

    stmt = select(User).join(User.addresses)

    result = session.execute(stmt)
    users = result.scalars().all()

    print("\n--- INNER JOIN ---")

    for user in users:
        print(user.name)

    # ------------------------------------------------------------------------------
    # 2. JOIN + SELECT BOTH MODELS - Returns both User and Address objects.
    # ------------------------------------------------------------------------------

    stmt = select(User, Address).join(User.addresses)

    result = session.execute(stmt)

    print("\n--- USER + ADDRESS ---")

    for user, address in result:
        print(user.name, "→", address.city)

    # ------------------------------------------------------------------------------
    # 3. JOIN + WHERE - Returns users whose address city is Delhi.
    # ------------------------------------------------------------------------------

    stmt = select(User).join(User.addresses).where(Address.city == "Delhi")

    result = session.execute(stmt)
    users = result.scalars().all()

    print("\n--- USERS IN DELHI ---")

    for user in users:
        print(user.name)

    # ------------------------------------------------------------------------------
    # 4. LEFT OUTER JOIN - Keeps users even when they do not have an address.
    # ------------------------------------------------------------------------------

    stmt = select(User, Address).outerjoin(User.addresses)

    result = session.execute(stmt)

    print("\n--- LEFT OUTER JOIN ---")

    for user, address in result:

        if address:
            print(user.name, "→", address.city)
        else:
            print(user.name, "→ No Address")

    # ------------------------------------------------------------------------------
    # 5. REVERSE-SIDE JOIN - Start from Address and join its related User.
    # ------------------------------------------------------------------------------

    stmt = select(Address, User).join(Address.user)

    result = session.execute(stmt)

    print("\n--- ADDRESS → USER ---")

    for address, user in result:
        print(address.city, "→", user.name)
