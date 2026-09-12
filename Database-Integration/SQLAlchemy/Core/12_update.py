# ============================================================
#                                                       UPDATE
#
# update()  → Creates an UPDATE SQL statement
#
# values()  → Specifies the new values
#
# where()   → Selects which rows should be updated
#
# execute() → Executes the UPDATE statement
#
# commit()  → Makes the transaction permanent
# ============================================================

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    insert,
    update,
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
            }
        ]
    )


with engine.begin() as connection:

    # --------------------------------------------------------
    # 1. Update one column
    # --------------------------------------------------------

    stmt = (
        update(users)
        .where(users.c.id == 1)
        .values(name="Gaurav Panwar")
    )

    connection.execute(stmt)


    # --------------------------------------------------------
    # 2. Update multiple columns
    # --------------------------------------------------------

    stmt = (
        update(users)
        .where(users.c.id == 2)
        .values(
            name="Rahul Sharma",
            email="rahul@example.com"
        )
    )

    connection.execute(stmt)


    # --------------------------------------------------------
    # 3. Update multiple rows
    # --------------------------------------------------------

    stmt = (
        update(users)
        .where(users.c.id <= 2)
        .values(email="updated@example.com")
    )

    connection.execute(stmt)


    # --------------------------------------------------------
    # 4. Check updated data
    # --------------------------------------------------------

    result = connection.execute(
        select(users)
    )

    print("\nUpdated users:")

    for row in result:
        print(row)
