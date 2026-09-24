# ================================================================================
#                    SQLALCHEMY ORM — ASSOCIATION OBJECT
#
# Association Object is a pattern used for many-to-many relationships when
# the association table contains additional columns/data.
#
# Instead of using a simple secondary table, the association table becomes a full ORM model.
#
# Relationship structure: User ──< UserProject >── Project
#
# Important Concepts:
#
# Association Object  - Makes the many-to-many association table an ORM model.
# secondary           - Used for simple many-to-many relationships.
# back_populates      - Connects both sides of an ORM relationship.
# ForeignKey          - Creates database-level relationships.
# ================================================================================

from datetime import date

from sqlalchemy import URL, ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


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
    __tablename__ = "orm_association_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # User → UserProject
    project_links: Mapped[list["UserProject"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Project(Base):
    __tablename__ = "orm_association_projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # Project → UserProject
    user_links: Mapped[list["UserProject"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class UserProject(Base):
    __tablename__ = "orm_association_user_projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("orm_association_users.id")
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("orm_association_projects.id")
    )

    role: Mapped[str] = mapped_column(String(50))
    joined_at: Mapped[date] = mapped_column()

    # UserProject → User
    user: Mapped["User"] = relationship(
        back_populates="project_links"
    )

    # UserProject → Project
    project: Mapped["Project"] = relationship(
        back_populates="user_links"
    )


# Create tables
Base.metadata.create_all(engine)


with Session(engine) as session:

    # Create users
    user1 = User(name="Gaurav")
    user2 = User(name="Rahul")

    # Create projects
    project1 = Project(name="MEDiFLOW")
    project2 = Project(name="GymOS")

    # Create association objects
    user_project1 = UserProject(
        user=user1,
        project=project1,
        role="Backend Developer",
        joined_at=date(2026, 9, 1),
    )

    user_project2 = UserProject(
        user=user1,
        project=project2,
        role="API Developer",
        joined_at=date(2026, 9, 10),
    )

    user_project3 = UserProject(
        user=user2,
        project=project1,
        role="Frontend Developer",
        joined_at=date(2026, 9, 5),
    )

    session.add_all([
        user_project1,
        user_project2,
        user_project3,
    ])

    session.commit()

    # --------------------------------------------------------------------------
    # Access projects through association objects
    # --------------------------------------------------------------------------

    user = session.get(User, user1.id)

    for link in user.project_links:
        print(
            user.name,
            link.project.name,
            link.role,
            link.joined_at,
        )

    # --------------------------------------------------------------------------
    # Access users through association objects
    # --------------------------------------------------------------------------

    project = session.get(Project, project1.id)

    for link in project.user_links:
        print(
            project.name,
            link.user.name,
            link.role,
        )
