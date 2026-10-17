from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

import app.events
from app.database import SessionLocal
from app.enums import TaskPriority, TaskStatus
from app.models import Project, ProjectMember, Task, TaskAssignee, User
from app.queries.reports import task_counts_by_project, task_counts_by_status, task_counts_by_user
from app.queries.tasks import list_overdue_tasks


def main() -> None:
    with SessionLocal() as session:
        print("\\n--- Users with project memberships ---")
        stmt = select(User).options(
            selectinload(User.project_memberships).selectinload(ProjectMember.project)
        ).order_by(User.id)
        for user in session.scalars(stmt).unique().all():
            projects = [membership.project.name for membership in user.project_memberships]
            print(user.name, "->", projects)

        print("\\n--- High priority tasks ---")
        stmt = select(Task).where(Task.priority.in_([TaskPriority.HIGH, TaskPriority.URGENT]))
        for task in session.scalars(stmt).all():
            print(task.id, task.title, task.priority.value)

        print("\\n--- Tasks with project and assignments loaded ---")
        stmt = select(Task).options(
            selectinload(Task.project),
            selectinload(Task.assignments).selectinload(TaskAssignee.user),
        ).order_by(Task.id)
        for task in session.scalars(stmt).all():
            assignees = [link.user.name for link in task.assignments]
            print(task.title, "| project:", task.project.name, "| assignees:", assignees)

        print("\\n--- Task counts by project ---")
        for project_name, count in task_counts_by_project():
            print(project_name, count)

        print("\\n--- Task counts by status for each project ---")
        projects = session.scalars(select(Project).order_by(Project.id)).all()
        for project in projects:
            print(project.name, task_counts_by_status(project.id))

        print("\\n--- Task counts by user ---")
        for user_name, count in task_counts_by_user():
            print(user_name, count)

        print("\\n--- Overdue tasks ---")
        overdue = list_overdue_tasks()
        if not overdue:
            print("No overdue tasks.")
        for task in overdue:
            print(task.title, task.due_date)

        total_tasks = session.scalar(select(func.count(Task.id)))
        print("\\nTotal tasks:", total_tasks)


if __name__ == "__main__":
    main()
