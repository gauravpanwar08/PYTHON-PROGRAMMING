from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import SessionLocal
from app.models import ProjectMember, User


def create_user(name: str, email: str) -> User:
    with SessionLocal.begin() as session:
        user = User(name=name, email=email)
        session.add(user)
        session.flush()
        session.refresh(user)
        return user


def get_user(user_id: int) -> User | None:
    with SessionLocal() as session:
        return session.get(User, user_id)


def list_active_users(limit: int = 50, offset: int = 0) -> list[User]:
    with SessionLocal() as session:
        stmt = (
            select(User)
            .where(User.is_active.is_(True))
            .order_by(User.id)
            .limit(limit)
            .offset(offset)
        )
        return list(session.scalars(stmt).all())


def get_user_with_memberships(user_id: int) -> User | None:
    with SessionLocal() as session:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.project_memberships).selectinload(ProjectMember.project))
        )
        return session.scalars(stmt).first()
