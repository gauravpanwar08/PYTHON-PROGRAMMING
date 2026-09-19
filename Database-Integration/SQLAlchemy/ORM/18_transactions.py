# ================================================================================
#                         SQLALCHEMY ORM — TRANSACTIONS
#
# A transaction is a group of database operations treated as one logical unit.
#
# All operations succeed → COMMIT
# Any operation fails → ROLLBACK
#
# Important Methods:
#
# session.begin()       - Starts a transaction and automatic commit/rollback the operations.
# session.commit()      - Permanently saves the transaction.
# session.rollback()    - Undoes uncommitted changes.
# session.flush()       - Sends pending changes to the database without committing.
# begin_nested()        - Creates a SAVEPOINT inside the current transaction.
# ================================================================================

from sqlalchemy import URL, create_engine, ForeignKey, String, Integer
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


class Order(Base):
    __tablename__ = "orm_orders_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100))

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderItem(Base):
    __tablename__ = "orm_order_items_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer)

    order_id: Mapped[int] = mapped_column(ForeignKey("orm_orders_transactions.id"))

    order: Mapped["Order"] = relationship(back_populates="items")


# Create tables
Base.metadata.create_all(engine)


# --------------------------------------------------------------------------------
# 1. BASIC TRANSACTION
# --------------------------------------------------------------------------------

with Session(engine) as session:

    with session.begin():

        order = Order(customer_name="Gaurav")

        item = OrderItem(
            product_name="Laptop",
            quantity=1,
        )

        order.items.append(item)

        session.add(order)

    # Transaction automatically committed here

    print("Order created successfully.")


# -------------------------------------------------------------------------------------
#  2. ROLLBACK - If an error occurs before commit, the transaction can be rolled back.
# -------------------------------------------------------------------------------------

with Session(engine) as session:

    try:

        with session.begin():

            order = Order(customer_name="Rahul")

            session.add(order)

            # Simulate an error
            raise ValueError("Something went wrong.")

    except ValueError as error:

        print("Transaction failed:", error)
        print("Transaction rolled back.")


# --------------------------------------------------------------------------------
# 3. MULTIPLE OPERATIONS IN ONE TRANSACTION
# --------------------------------------------------------------------------------

with Session(engine) as session:

    try:

        with session.begin():

            # Create order
            order = Order(customer_name="Aman")

            # Create multiple order items
            order.items = [
                OrderItem(
                    product_name="Keyboard",
                    quantity=1,
                ),
                OrderItem(
                    product_name="Mouse",
                    quantity=2,
                ),
            ]

            session.add(order)

            print("Order and items added to transaction.")

        print("Transaction committed successfully.")

    except Exception as error:

        print("Transaction failed:", error)


# --------------------------------------------------------------------------------
# 4. MANUAL COMMIT + ROLLBACK
#
# commit() saves changes and rollback() removes uncommitted changes.
# --------------------------------------------------------------------------------

with Session(engine) as session:

    try:

        order = Order(customer_name="Neha")

        session.add(order)

        # Permanently save changes
        session.commit()

        print("Order committed successfully.")

    except Exception as error:

        # Undo uncommitted changes
        session.rollback()

        print("Transaction rolled back:", error)


# --------------------------------------------------------------------------------
# 5. FLUSH VS COMMIT
#
# flush() → Sends pending changes to the database but Transaction is still active.
# commit() → Finalizes the transaction.
# --------------------------------------------------------------------------------

with Session(engine) as session:

    with session.begin():

        order = Order(customer_name="Priya")

        session.add(order)

        # Send INSERT to database
        session.flush()

        # Generated primary key is now available
        print("Order ID after flush:", order.id)

    # Transaction committed here


# -------------------------------------------------------------------------------------------
# 6. NESTED TRANSACTION : 
#
# begin_nested() creates a SAVEPOINT inside the current transaction.
# If nested operation fails → Roll back to SAVEPOINT and Outer transaction can continue.
# --------------------------------------------------------------------------------------------

with Session(engine) as session:

    with session.begin():

        order = Order(customer_name="Vikas")

        session.add(order)

        session.flush()

        print("Outer transaction - Order ID:", order.id)

        try:

            with session.begin_nested():

                item = OrderItem(
                    product_name="Monitor",
                    quantity=1,
                    order_id=order.id,
                )

                session.add(item)

                # Simulate nested operation failure
                raise ValueError("Nested operation failed.")

        except ValueError as error:

            print("Nested transaction rolled back:", error)

        # Outer transaction continues
        print("Outer transaction is still active.")
