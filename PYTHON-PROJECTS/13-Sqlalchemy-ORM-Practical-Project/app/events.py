from datetime import datetime, timezone

from sqlalchemy import event
from sqlalchemy.orm import Session

from app.enums import TaskStatus
from app.models import Comment, Task, User


@event.listens_for(User, "before_insert")
@event.listens_for(User, "before_update")
def normalize_user(mapper, connection, target: User) -> None:
    target.name = target.name.strip()
    target.email = target.email.strip().lower()


@event.listens_for(Task, "before_insert")
@event.listens_for(Task, "before_update")
def update_task_completion_time(mapper, connection, target: Task) -> None:
    if target.status == TaskStatus.DONE and target.completed_at is None:
        target.completed_at = datetime.now(timezone.utc)
    elif target.status != TaskStatus.DONE:
        target.completed_at = None


@event.listens_for(Session, "before_flush")
def validate_pending_objects(session: Session, flush_context, instances) -> None:
    for obj in session.new:
        if isinstance(obj, Comment) and not obj.content.strip():
            raise ValueError("Comment content cannot be blank")
