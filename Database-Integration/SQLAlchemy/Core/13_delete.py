# ============================================================
#                                                       DELETE
#
# delete()  → Creates a DELETE SQL statement
#
# where()   → Specifies which rows should be deleted
#
# execute() → Executes the DELETE statement
#
# engine.begin() → Manages connection and transaction
#
# ⚠️ Without where() → All rows are deleted
# ============================================================

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    insert,
    delete,
    select
)

DATABASE_URL = "sqlite:///example.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String)
)

metadata.create_all(engine)

with engine.begin() as connection:
    connection.execute(
        insert(users),
        [
            {
                "name": "Gaurav",
                "email": "gaurav@example.com"
            },
            {
                "name": "Rahul",
                "email": "rahul@example.com"
            },
            {
                "name": "Aman",
                "email": "aman@example.com"
            },
            {
                "name": "Rohit",
                "email": "rohit@example.com"
            }
        ]
    )


with engine.begin() as connection:

    # --------------------------------------------------------
    # 1. Delete one row
    # --------------------------------------------------------

    stmt = (
        delete(users)
        .where(users.c.id == 1)
    )

    connection.execute(stmt)


    # --------------------------------------------------------
    # 2. Delete multiple rows
    # --------------------------------------------------------

    stmt = (
        delete(users)
        .where(users.c.id >= 3)
    )

    connection.execute(stmt)


    # --------------------------------------------------------
    # 3. Check remaining data
    # --------------------------------------------------------

    result = connection.execute(
        select(users)
    )

    print("\nRemaining users:")

    for row in result:
        print(row)