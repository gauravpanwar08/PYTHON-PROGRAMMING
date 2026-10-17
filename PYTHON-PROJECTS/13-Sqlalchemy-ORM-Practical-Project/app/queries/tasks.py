from datetime import datetime, timezone

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.database import SessionLocal
from app.enums import TaskPriority, TaskStatus
from app.models import Comment, Task, TaskAssignee, User


def create_task(
    project_id: int,
    title: str,
    priority: TaskPriority = TaskPriority.MEDIUM,
    due_date: datetime | None = None,
    estimated_hours: float | None = None,
) -> int:
    with SessionLocal.begin() as session:
        task = Task(
            project_id=project_id,
            title=title,
            priority=priority,
            due_date=due_date,
            estimated_hours=estimated_hours,
        )
        session.add(task)
        session.flush()
        return task.id


def assign_user(task_id: int, user_id: int) -> None:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)
        user = session.get(User, user_id)
        if task is None or user is None:
            raise ValueError("Task and user must both exist")
        task.assignments.append(TaskAssignee(user=user))


def add_comment(task_id: int, user_id: int, content: str) -> None:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)
        user = session.get(User, user_id)
        if task is None or user is None:
            raise ValueError("Task and user must both exist")
        task.comments.append(Comment(author=user, content=content))


def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Task]:
    with SessionLocal() as session:
        stmt = select(Task).options(selectinload(Task.project)).order_by(Task.id)
        if status is not None:
            stmt = stmt.where(Task.status == status)
        if priority is not None:
            stmt = stmt.where(Task.priority == priority)
        stmt = stmt.limit(limit).offset(offset)
        return list(session.scalars(stmt).all())


def list_overdue_tasks() -> list[Task]:
    with SessionLocal() as session:
        stmt = (
            select(Task)
            .where(Task.is_overdue.is_(True))
            .options(selectinload(Task.project))
            .order_by(Task.due_date)
        )
        return list(session.scalars(stmt).all())


def complete_task(task_id: int) -> bool:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)
        if task is None:
            return False
        task.status = TaskStatus.DONE
        return True


def bulk_cancel_todo_tasks(project_id: int) -> int:
    with SessionLocal.begin() as session:
        stmt = (
            update(Task)
            .where(Task.project_id == project_id, Task.status == TaskStatus.TODO)
            .values(status=TaskStatus.CANCELLED)
            .execution_options(synchronize_session="fetch")
        )
        result = session.execute(stmt)
        return result.rowcount or 0


def delete_task(task_id: int) -> bool:
    with SessionLocal.begin() as session:
        task = session.get(Task, task_id)
        if task is None:
            return False
        session.delete(task)
        return True
