# =======================================================================================
#                            TRANSACTIONS
#
# Transaction : A group of database operations treated as one logical unit.
#
# engine.begin()        → Starts a transaction and automatically commits/rollback.
# connection.begin()    → Starts a transaction with manual commit/rollback control.
# commit()              → Permanently saves transaction changes.
# rollback()            → Reverts changes made in the current transaction.
# begin_nested()        → Creates a SAVEPOINT inside an existing transaction.
#
# Transaction Flow:
#   Operations successful → COMMIT
#   Any operation fails   → ROLLBACK
# ========================================================================================


from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    select,
)


# Create engine
engine = create_engine("sqlite:///transactions.db")

# Create metadata
metadata = MetaData()


# Create accounts table
accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("balance", Float, nullable=False),
)


# Create table in database
metadata.create_all(engine)


# Insert sample data
account_data = [
    {"id": 1, "balance": 10000},
    {"id": 2, "balance": 5000},
]

with engine.begin() as connection:
    connection.execute(accounts.insert(), account_data)


# -------------------------------------------------------------------
# engine.begin() - Automatically commits on success.
# -------------------------------------------------------------------

with engine.begin() as connection:
    connection.execute(
        accounts.update()
        .where(accounts.c.id == 1)
        .values(balance=9000)
    )

    connection.execute(
        accounts.update()
        .where(accounts.c.id == 2)
        .values(balance=6000)
    )


# Execute query
with engine.connect() as connection:
    result = connection.execute(
        select(accounts)
    )

    for row in result:
        print(row)


# -------------------------------------------------------------------
# connection.begin() - Manual commit.
# -------------------------------------------------------------------

with engine.connect() as connection:
    transaction = connection.begin()

    try:
        connection.execute(
            accounts.update()
            .where(accounts.c.id == 1)
            .values(balance=8000)
        )
        transaction.commit()

    except:
        transaction.rollback()
        raise


# -------------------------------------------------------------------
# ROLLBACK - Undo changes when an operation fails.
# -------------------------------------------------------------------

with engine.connect() as connection:
    transaction = connection.begin()

    try:
        connection.execute(
            accounts.update()
            .where(accounts.c.id == 1)
            .values(balance=7000)
        )

        raise ValueError("Something went wrong")
        transaction.commit()


    except:
        transaction.rollback()


# Execute query
with engine.connect() as connection:
    result = connection.execute(
        select(accounts)
    )

    for row in result:
        print(row)


# -------------------------------------------------------------------
# begin_nested() - Create a SAVEPOINT inside a transaction.
# -------------------------------------------------------------------

with engine.connect() as connection:
    transaction = connection.begin()

    try:
        connection.execute(
            accounts.update()
            .where(accounts.c.id == 1)
            .values(balance=8500)
        )

        savepoint = connection.begin_nested()

        try:
            connection.execute(
                accounts.update()
                .where(accounts.c.id == 2)
                .values(balance=6500)
            )

            savepoint.commit()

        except:
            savepoint.rollback()

        transaction.commit()

    except:
        transaction.rollback()
        raise


# Generated SQL
print(
    accounts.update()
    .where(accounts.c.id == 1)
    .values(balance=9000)
)
