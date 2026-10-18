
# Implement create and read user APIs using SQLAlchemy ORM.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# Create User
# Insert a new user and return the saved database record.

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    user = User(
        name=user_data.name,
        email=str(user_data.email),
        age=user_data.age,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from exc

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user",
        ) from exc


# Read All Users
# Retrieve all users from the database.

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    statement = select(User).order_by(User.id)
    result = db.scalars(statement).all()

    return result


# Read User By ID
# Retrieve one user by its primary key.

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    statement = select(User).where(User.id == user_id)
    user = db.scalar(statement)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# Update User
# Replace editable user fields and save the changes.

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.name = user_data.name
    user.email = str(user_data.email)
    user.age = user_data.age

    try:
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        ) from exc

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update user",
        ) from exc


# Delete User
# Delete an existing user from PostgreSQL.

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    try:
        db.delete(user)
        db.commit()

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete user",
        ) from exc
