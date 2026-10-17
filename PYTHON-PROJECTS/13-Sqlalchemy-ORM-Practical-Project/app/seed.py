from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.database import SessionLocal
from app.enums import ProjectStatus, TaskPriority, TaskStatus
from app.models import Comment, Project, ProjectMember, Task, TaskAssignee, User
import app.events


def seed() -> None:
    with SessionLocal.begin() as session:
        users_by_email = {}
        for name, email in [
            ("Gaurav Panwar", "gaurav@example.com"),
            ("Rahul Sharma", "rahul@example.com"),
            ("Aman Verma", "aman@example.com"),
        ]:
            user = session.scalar(select(User).where(User.email == email))
            if user is None:
                user = User(name=name, email=email)
                session.add(user)
                session.flush()
            users_by_email[email] = user

        projects_by_name = {}
        for name, description in [
            ("MEDiFLOW", "Hospital management backend"),
            ("IronCore-GymOS", "Gym operations platform"),
        ]:
            project = session.scalar(select(Project).where(Project.name == name))
            if project is None:
                project = Project(name=name, description=description, status=ProjectStatus.ACTIVE)
                session.add(project)
                session.flush()
            projects_by_name[name] = project

        membership_specs = [
            ("gaurav@example.com", "MEDiFLOW", "Backend Developer"),
            ("rahul@example.com", "MEDiFLOW", "Frontend Developer"),
            ("gaurav@example.com", "IronCore-GymOS", "Backend Developer"),
            ("aman@example.com", "IronCore-GymOS", "QA Engineer"),
        ]
        for email, project_name, role in membership_specs:
            user, project = users_by_email[email], projects_by_name[project_name]
            exists = session.scalar(
                select(ProjectMember.id).where(
                    ProjectMember.user_id == user.id,
                    ProjectMember.project_id == project.id,
                )
            )
            if exists is None:
                session.add(ProjectMember(user=user, project=project, role=role))

        task_specs = [
            ("MEDiFLOW", "Build authentication API", TaskPriority.HIGH, TaskStatus.IN_PROGRESS, 8.0),
            ("MEDiFLOW", "Implement appointment endpoints", TaskPriority.URGENT, TaskStatus.TODO, 12.0),
            ("IronCore-GymOS", "Create membership module", TaskPriority.MEDIUM, TaskStatus.DONE, 6.0),
        ]
        tasks_by_title = {}
        for project_name, title, priority, status, hours in task_specs:
            task = session.scalar(select(Task).where(Task.title == title))
            if task is None:
                task = Task(
                    project=projects_by_name[project_name],
                    title=title,
                    priority=priority,
                    status=status,
                    estimated_hours=hours,
                    due_date=datetime.now(timezone.utc) + timedelta(days=7),
                )
                session.add(task)
                session.flush()
            tasks_by_title[title] = task

        assignments = [
            ("Build authentication API", "gaurav@example.com"),
            ("Implement appointment endpoints", "gaurav@example.com"),
            ("Implement appointment endpoints", "rahul@example.com"),
            ("Create membership module", "aman@example.com"),
        ]
        for title, email in assignments:
            task, user = tasks_by_title[title], users_by_email[email]
            exists = session.scalar(
                select(TaskAssignee.id).where(
                    TaskAssignee.task_id == task.id,
                    TaskAssignee.user_id == user.id,
                )
            )
            if exists is None:
                session.add(TaskAssignee(task=task, user=user))

        comment_specs = [
            ("Build authentication API", "gaurav@example.com", "Initial endpoint structure is ready."),
            ("Implement appointment endpoints", "rahul@example.com", "I will review the request schemas."),
        ]
        for title, email, content in comment_specs:
            task, user = tasks_by_title[title], users_by_email[email]
            exists = session.scalar(
                select(Comment.id).where(
                    Comment.task_id == task.id,
                    Comment.user_id == user.id,
                    Comment.content == content,
                )
            )
            if exists is None:
                session.add(Comment(task=task, author=user, content=content))


if __name__ == "__main__":
    import app.events

    seed()
    print("Seed data created/verified.")
