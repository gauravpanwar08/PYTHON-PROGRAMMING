from sqlalchemy import func, select

from app.database import SessionLocal
from app.enums import TaskStatus
from app.models import Project, Task, TaskAssignee, User


def task_counts_by_status(project_id: int) -> list[tuple[TaskStatus, int]]:
    with SessionLocal() as session:
        stmt = (
            select(Task.status, func.count(Task.id))
            .where(Task.project_id == project_id)
            .group_by(Task.status)
            .order_by(Task.status)
        )
        return list(session.execute(stmt).all())


def task_counts_by_project() -> list[tuple[str, int]]:
    with SessionLocal() as session:
        stmt = (
            select(Project.name, func.count(Task.id))
            .outerjoin(Project.tasks)
            .group_by(Project.id, Project.name)
            .order_by(Project.name)
        )
        return list(session.execute(stmt).all())


def task_counts_by_user() -> list[tuple[str, int]]:
    with SessionLocal() as session:
        stmt = (
            select(User.name, func.count(TaskAssignee.task_id))
            .outerjoin(User.task_assignments)
            .group_by(User.id, User.name)
            .order_by(User.name)
        )
        return list(session.execute(stmt).all())
