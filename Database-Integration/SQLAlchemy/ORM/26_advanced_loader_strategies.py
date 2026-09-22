# ================================================================================
#                    SQLALCHEMY ORM — ADVANCED LOADER STRATEGIES
#
# Advanced loader strategies control how related ORM objects are loaded.
# They help avoid unnecessary queries and improve ORM query performance.
#
# Important Loader Strategies:
#
# selectinload()    - Loads related objects using a separate IN query.
# joinedload()      - Loads related objects using JOIN.
# subqueryload()    - Loads related objects using a separate subquery.
# lazyload()        - Forces lazy loading for a relationship.
# noload()          - Prevents loading a relationship.
# raiseload()       - Raises an error when an unloaded relationship is accessed.
# defaultload()     - Applies loading options deeper in a relationship path.
# contains_eager()  - Uses an explicit JOIN to populate a relationship.
# ================================================================================


from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    sessionmaker,
    contains_eager,
    defaultload,
    joinedload,
    lazyload,
    mapped_column,
    noload,
    raiseload,
    relationship,
    selectinload,
    subqueryload,
)


# Create engine
engine = create_engine(
    "postgresql+psycopg://postgres:aura123@localhost:5432/sqlalchemy_db",
    echo=True,
)


# Create Declarative Base
class Base(DeclarativeBase):
    pass


# Create User model
class User(Base):
    __tablename__ = "advanced_loader_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user"
    )


# Create Order model
class Order(Base):
    __tablename__ = "advanced_loader_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("advanced_loader_users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="orders"
    )


# Create tables
Base.metadata.create_all(engine)

# Create Session factory
SessionLocal = sessionmaker(bind=engine)


with SessionLocal() as session:

    # Insert sample data
    user1 = User(
        name="Gaurav",
        orders=[
            Order(product="Laptop"),
            Order(product="Keyboard"),
        ],
    )

    user2 = User(
        name="Rahul",
        orders=[
            Order(product="Mouse"),
        ],
    )

    user3 = User(
        name="Aman",
        orders=[],
    )

    session.add_all([user1, user2, user3])
    session.commit()


    # ----------------------------------------------------------------
    # selectinload() - Loads related objects using a separate IN query.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .options(selectinload(User.orders))
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name, user.orders)


    # ----------------------------------------------------------------
    # joinedload() - Loads related objects using JOIN.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .options(joinedload(User.orders))
    )

    result = session.execute(stmt)

    # unique() is required when joinedload() loads a collection.
    users = result.unique().scalars().all()

    for user in users:
        print(user.name, user.orders)


    # ----------------------------------------------------------------
    # subqueryload() - Loads relationships using a separate subquery.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .options(subqueryload(User.orders))
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name, user.orders)


    # ----------------------------------------------------------------
    # lazyload() - Loads the relationship only when it is accessed.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .options(lazyload(User.orders))
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name)

        # Relationship query happens here.
        print(user.orders)


    # ----------------------------------------------------------------
    # noload() - Prevents SQLAlchemy from loading the relationship.
    # ----------------------------------------------------------------

    stmt = (
        select(User)
        .options(noload(User.orders))
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name)
        print(user.orders)


    # -----------------------------------------------------------------------------------------------
    # raiseload() - Raises an error if the relationship is accessed without being explicitly loaded.
    # -----------------------------------------------------------------------------------------------

    stmt = (
        select(User)
        .options(raiseload(User.orders))
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name)

        # This raises an exception because orders were not loaded.
        # print(user.orders)


    # -------------------------------------------------------------------------------
    # defaultload() - Applies another loading strategy deeper in a relationship path.
    # --------------------------------------------------------------------------------

    stmt = (
        select(User)
        .options(
            defaultload(User.orders).selectinload(Order.user)
        )
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name, user.orders)


    # ------------------------------------------------------------------------------------------
    # Nested selectinload() - Loads relationships at multiple levels. e.g.- User → Orders → User
    # -------------------------------------------------------------------------------------------

    stmt = (
        select(User)
        .options(
            selectinload(User.orders)
            .selectinload(Order.user)
        )
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name)

        for order in user.orders:
            print(order.product, order.user.name)


    # -----------------------------------------------------------------------------------------
    # Multiple loader options - Different relationships can have different loading strategies.
    # -----------------------------------------------------------------------------------------

    stmt = (
        select(User)
        .options(
            selectinload(User.orders),
            raiseload("*"),
        )
    )

    users = session.scalars(stmt).all()

    for user in users:
        print(user.name, user.orders)


    # -------------------------------------------------------------------------------------------------------
    # contains_eager() - Tells SQLAlchemy that an explicit JOIN should be used to populate the relationship.
    # -------------------------------------------------------------------------------------------------------

    stmt = (
        select(User)
        .join(User.orders)
        .where(Order.product == "Laptop")
        .options(contains_eager(User.orders))
    )

    result = session.execute(stmt)

    users = result.unique().scalars().all()

    for user in users:
        print(user.name, user.orders)


    # --------------------------------------------------------------------------------
    # join() vs contains_eager()
    #
    # join() controls which rows are selected.
    # contains_eager() tells ORM to populate the relationship from that explicit JOIN.
    # ----------------------------------------------------------------------------------

    stmt = (
        select(User)
        .join(User.orders)
        .where(Order.product == "Keyboard")
        .options(contains_eager(User.orders))
    )

    result = session.execute(stmt)

    users = result.unique().scalars().all()

    for user in users:
        print(user.name, user.orders)
