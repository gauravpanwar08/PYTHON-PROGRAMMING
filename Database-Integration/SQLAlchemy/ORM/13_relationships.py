# ========================================================================================================
#                       SQLALCHEMY ORM — RELATIONSHIPS
#
# A relationship connects records between two ORM models.
# relationship(...)  -  Creates the ORM-level object relationship.
# ForeignKey(...)    -  Creates the database-level relationship.
# back_populates     -  Connects relationship attributes on both models.
#
# Important Parameters:
#
# argument       → Target ORM model/class that this relationship connects to.
# back_populates → Explicitly links the relationship from both sides of the models.
# backref        → Automatically creates the reverse relationship on the related model.
# secondary      → Specifies the association table used for many-to-many relationships.
# uselist        → Controls whether the relationship returns a collection (list) or a single ORM object.
# cascade        → Defines how operations on a parent object affect its related objects.
# lazy           → Controls when and how related objects are loaded from the database.
# primaryjoin    → Defines the primary SQL join condition used by the relationship.
# order_by       → Defines the ordering of related objects when they are loaded.
# =========================================================================================================


from sqlalchemy import ForeignKey, String, URL, create_engine, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy.orm import mapped_column, relationship, sessionmaker

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


# DeclarativeBase


class Base(DeclarativeBase):
    pass


# ----------------------------------------------------------------------------
# ONE-TO-MANY or MANY-TO-ONE RELATIONSHIP:
#
# One User can have Many Addresses and Many Addresses can have One User
# ----------------------------------------------------------------------------


class User(Base):
    __tablename__ = "orm_users_relationship"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "orm_addresses_relationship"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey("orm_users_relationship.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")


# Create tables
Base.metadata.create_all(engine)


# Create Session factory
SessionLocal = sessionmaker(bind=engine)


# Create User + Addresses

with SessionLocal() as session:

    user = User(name="Gaurav")

    address1 = Address(city="Dehradun")
    address2 = Address(city="Delhi")

    user.addresses = [address1, address2]

    session.add(user)

    session.commit()

    print("\nUser and addresses inserted.")

    print("User ID:", user.id)
    print("Address 1 ID:", address1.id)
    print("Address 2 ID:", address2.id)

# Access Addresses through User

with SessionLocal() as session:

    user = session.get(User, 1)

    if user:

        print("\nUser:")
        print(user.name)

        print("\nAddresses:")

        for address in user.addresses:
            print(address.id, address.city)


# Access User through Address

with SessionLocal() as session:

    address = session.get(Address, 1)

    if address:

        print("\nAddress:")
        print(address.city)

        print("\nUser:")
        print(address.user.name)


print("\nRelationship operation completed.")

# ---------------------------------------------------------------------------------
# ONE-TO-ONE RELATIONSHIP:
#
# One User has exactly one Profile and One Profile belongs to exactly one User.
# uselist=False → Makes the relationship return a single object instead of a list.
# ----------------------------------------------------------------------------------


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    profile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="profile")


# Create user and profile

with SessionLocal() as session:
    user = User(name="Gaurav")

profile = UserProfile(bio="Python Backend Developer")

user.profile = profile

session.add(user)
session.commit()

# Access profile from user
print(user.profile.bio)

# Access user from profile
print(profile.user.name)


# -----------------------------------------------------------------------
# MANY-TO-MANY RELATIONSHIP:
#
# One User can have many Course and One Course can have many Users.
# secondary → Specifies the association table connecting both models.
# -----------------------------------------------------------------------

user_course = Table(
    "user_course",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    courses: Mapped[list["Course"]] = relationship(
        secondary=user_course, back_populates="users"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    users: Mapped[list["User"]] = relationship(
        secondary=user_course, back_populates="courses"
    )


# Create user
with SessionLocal() as session:
    user = User(name="Gaurav")

# Create courses
course1 = Course(title="Python")
course2 = Course(title="SQLAlchemy")

# Assign courses to user
user.courses = [course1, course2]

session.add(user)
session.commit()

# User → Courses
for course in user.courses:
    print(course.title)

# Course → Users
for user in course1.users:
    print(user.name)
