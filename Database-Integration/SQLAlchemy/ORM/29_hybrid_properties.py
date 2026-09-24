# ================================================================================
#                    SQLALCHEMY ORM — HYBRID PROPERTIES
#
# Hybrid properties are calculated ORM attributes that can work both:
# 1. On Python objects and 2. Inside SQLAlchemy SQL expressions
#
# Syntax : @hybrid_property

# Important Methods / Concepts:
#
# hybrid_property      - Creates an attribute usable on Python objects and queries.
# expression           - Defines the SQL expression used by the hybrid property.
# inplace.expression   - Defines/modifies the SQL expression in-place.
# ================================================================================

from sqlalchemy import URL, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.ext.hybrid import hybrid_property


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
    __tablename__ = "orm_users_hybrid"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]

    # --------------------------------------------------------------------------
    # hybrid_property - Calculated attribute usable in Python and SQL queries.
    # --------------------------------------------------------------------------

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # --------------------------------------------------------------------------
    # expression - Defines the SQL expression for the hybrid property.
    # --------------------------------------------------------------------------

    @full_name.expression
    def full_name(cls):
        return cls.first_name + " " + cls.last_name

    @hybrid_property
    def is_adult(self):
        return self.age >= 18

    @is_adult.expression
    def is_adult(cls):
        return cls.age >= 18


# Create table
Base.metadata.create_all(engine)


with Session(engine) as session:

    # Insert sample data
    users = [
        User(first_name="Gaurav", last_name="Panwar", age=22),
        User(first_name="Rahul", last_name="Sharma", age=17),
        User(first_name="Aman", last_name="Verma", age=25),
    ]

    session.add_all(users)
    session.commit()

    # --------------------------------------------------------------------------
    # Python-side hybrid property
    # --------------------------------------------------------------------------

    user = users[0]

    print(user.full_name)
    print(user.is_adult)

    # --------------------------------------------------------------------------
    # SQL-side hybrid property
    # --------------------------------------------------------------------------

    stmt = select(User).where(User.full_name == "Gaurav Panwar")

    result = session.scalars(stmt).all()

    for user in result:
        print(user.id, user.full_name)

    # --------------------------------------------------------------------------
    # SQL-side boolean hybrid property
    # --------------------------------------------------------------------------

    stmt = select(User).where(User.is_adult.is_(True))

    adult_users = session.scalars(stmt).all()

    for user in adult_users:
        print(user.full_name, user.age)
