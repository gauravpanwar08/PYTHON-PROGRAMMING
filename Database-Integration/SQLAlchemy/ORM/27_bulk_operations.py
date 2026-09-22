# ================================================================================
#                    SQLALCHEMY ORM — BULK OPERATIONS
#
# Bulk operations are used to efficiently process multiple database rows.
# They can reduce Python-side ORM object overhead for large/simple operations.
#
# Important Methods / Concepts:
#
# session.execute()   - Executes SQLAlchemy Core/ORM statements through Session.
# insert()            - Creates an INSERT statement.
# update()            - Creates an UPDATE statement.
# delete()            - Creates a DELETE statement.
# returning()         - Returns values from affected rows.
# synchronize_session - Controls synchronization of ORM objects after bulk UPDATE/DELETE operations.
#
# Bulk operations are useful for large/simple data operations.
# Normal ORM operations are preferable when object tracking and relationships are important.
# ===================================================================================================


from sqlalchemy import (
    String,
    create_engine,
    delete,
    insert,
    select,
    update,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    sessionmaker,
    mapped_column,
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
    __tablename__ = "bulk_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)


# Create tables
Base.metadata.create_all(engine)

# Create Session factory
SessionLocal = sessionmaker(bind=engine)


with SessionLocal() as session:

    # ----------------------------------------------------------------
    # Bulk INSERT - Insert multiple rows using parameter dictionaries.
    # ----------------------------------------------------------------

    stmt = insert(User)

    session.execute(
        stmt,
        [
            {
                "name": "Gaurav",
                "email": "gaurav_bulk@example.com",
                "age": 22,
            },
            {
                "name": "Rahul",
                "email": "rahul_bulk@example.com",
                "age": 24,
            },
            {
                "name": "Aman",
                "email": "aman_bulk@example.com",
                "age": 17,
            },
        ],
    )

    session.commit()


    # ----------------------------------------------------------------
    # Read inserted data.
    # ----------------------------------------------------------------

    users = session.scalars(
        select(User)
    ).all()

    for user in users:
        print(user.id, user.name, user.age)


    # ----------------------------------------------------------------
    # Bulk INSERT with RETURNING - Returns database-generated values.
    # ----------------------------------------------------------------

    stmt = (
        insert(User)
        .returning(User.id, User.name)
    )

    result = session.execute(
        stmt,
        [
            {
                "name": "Neeraj",
                "email": "neeraj_bulk@example.com",
                "age": 25,
            },
            {
                "name": "Vikas",
                "email": "vikas_bulk@example.com",
                "age": 23,
            },
        ],
    )

    returned_rows = result.all()

    session.commit()

    for row in returned_rows:
        print(row.id, row.name)


    # ----------------------------------------------------------------
    # Bulk UPDATE - Update multiple matching rows directly in database.
    # ----------------------------------------------------------------

    stmt = (
        update(User)
        .where(User.age < 18)
        .values(age=18)
    )

    result = session.execute(stmt)

    session.commit()

    print("Updated rows:", result.rowcount)


    # ----------------------------------------------------------------
    # Bulk UPDATE with synchronize_session
    #
    # synchronize_session="fetch" tells SQLAlchemy to synchronize
    # ORM objects already present in the Session with database changes.
    # ----------------------------------------------------------------

    stmt = (
        update(User)
        .where(User.age >= 18)
        .values(age=30)
        .execution_options(synchronize_session="fetch")
    )

    result = session.execute(stmt)

    session.commit()

    print("Updated rows:", result.rowcount)


    # ----------------------------------------------------------------
    # Bulk DELETE - Delete multiple rows matching a condition.
    # ----------------------------------------------------------------

    stmt = (
        delete(User)
        .where(User.age < 20)
        .execution_options(synchronize_session="fetch")
    )

    result = session.execute(stmt)

    session.commit()

    print("Deleted rows:", result.rowcount)


    # ----------------------------------------------------------------
    # synchronize_session=False
    #
    # SQLAlchemy does not try to synchronize ORM objects already
    # present in the Session with the database changes.
    # ----------------------------------------------------------------

    stmt = (
        update(User)
        .where(User.name == "Gaurav")
        .values(age=35)
        .execution_options(synchronize_session=False)
    )

    session.execute(stmt)

    session.commit()


    # ----------------------------------------------------------------
    # Verify final data.
    # ----------------------------------------------------------------

    users = session.scalars(
        select(User)
    ).all()

    for user in users:
        print(
            user.id,
            user.name,
            user.email,
            user.age,
        )
