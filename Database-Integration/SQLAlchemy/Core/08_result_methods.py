# ====================================================================
#                      RESULT METHODS
#
# Result → Object containing rows returned by execute()

# all()         → Returns all remaining rows as a list
# first()       → Returns the first row or None
# one()         → Returns exactly one row
# one_or_none() → Returns one row or None
# scalar()      → Returns the first column of the first row
# scalars()     → Extracts values from the first selected column
# fetchone()    → Returns one row
# fetchmany()   → Returns a limited number of rows
# =====================================================================

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    insert,
    select
)

DATABASE_URL = "sqlite:///example.db"

engine = create_engine(
    DATABASE_URL
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

with engine.connect() as connection:

    # --------------------------------------------------------
    # 1. all()
    # --------------------------------------------------------

    result = connection.execute(
        select(users)
    )

    rows = result.all()

    print("\nall():")
    print(rows)


    # --------------------------------------------------------
    # 2. first()
    # --------------------------------------------------------

    result = connection.execute(
        select(users)
    )

    row = result.first()

    print("\nfirst():")
    print(row)


    # --------------------------------------------------------
    # 3. one()
    # --------------------------------------------------------

    result = connection.execute(
        select(users).where(users.c.id == 1)
    )

    row = result.one()

    print("\none():")
    print(row)


    # --------------------------------------------------------
    # 4. one_or_none()
    # --------------------------------------------------------

    result = connection.execute(
        select(users).where(users.c.id == 100)
    )

    row = result.one_or_none()

    print("\none_or_none():")
    print(row)


    # --------------------------------------------------------
    # 5. scalar()
    # --------------------------------------------------------

    result = connection.execute(
        select(users.c.name).where(users.c.id == 1)
    )

    value = result.scalar()

    print("\nscalar():")
    print(value)


    # --------------------------------------------------------
    # 6. scalars()
    # --------------------------------------------------------

    result = connection.execute(
        select(users.c.name)
    )

    names = result.scalars().all()

    print("\nscalars():")
    print(names)


    # --------------------------------------------------------
    # 7. fetchone()
    # --------------------------------------------------------

    result = connection.execute(
        select(users)
    )

    row = result.fetchone()

    print("\nfetchone():")
    print(row)


    # --------------------------------------------------------
    # 8. fetchmany()
    # --------------------------------------------------------

    result = connection.execute(
        select(users)
    )

    rows = result.fetchmany(2)

    print("\nfetchmany():")
    print(rows)
