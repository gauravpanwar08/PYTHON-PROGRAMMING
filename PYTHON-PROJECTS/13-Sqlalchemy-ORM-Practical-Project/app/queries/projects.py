from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import SessionLocal
from app.models import Project, ProjectMember, User
from app.enums import ProjectStatus


def create_project(name: str, description: str | None = None) -> Project:
    with SessionLocal.begin() as session:
        project = Project(name=name, description=description)
        session.add(project)
        session.flush()
        session.refresh(project)
        return project


def add_project_member(user_id: int, project_id: int, role: str) -> None:
    with SessionLocal.begin() as session:
        user = session.get(User, user_id)
        project = session.get(Project, project_id)
        if user is None or project is None:
            raise ValueError("User and project must both exist")
        session.add(ProjectMember(user=user, project=project, role=role))


def list_projects_with_tasks() -> list[Project]:
    with SessionLocal() as session:
        stmt = select(Project).options(selectinload(Project.tasks)).order_by(Project.id)
        return list(session.scalars(stmt).all())


def set_project_status(project_id: int, status: ProjectStatus) -> bool:
    with SessionLocal.begin() as session:
        project = session.get(Project, project_id)
        if project is None:
            return False
        project.status = status
        return True
