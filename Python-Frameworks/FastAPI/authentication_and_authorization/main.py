
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.authorization import AdminUser
from auth.dependencies import CurrentUser
from auth.password_hashing import hash_password, verify_password
from auth.refresh_tokens import (
    generate_refresh_token,
    hash_refresh_token,
)
from auth.schemas import (
    RefreshRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from auth.token import create_access_token
from core.config import settings
from db.database import Base, engine
from db.dependencies import get_db
from models.user import User
from models.refresh_token import RefreshToken
from models.password_reset_token import PasswordResetToken

# Learning/development only. Production projects should use Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Authentication Integration")


def create_refresh_record(
    user_id: int,
    family_id: str,
) -> tuple[str, RefreshToken]:
    raw_token = generate_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )

    record = RefreshToken(
        user_id=user_id,
        token_hash=hash_refresh_token(raw_token),
        family_id=family_id,
        expires_at=expires_at,
    )

    return raw_token, record


def revoke_token_family(
    db: Session,
    family_id: str,
    now: datetime,
) -> None:
    records = db.scalars(
        select(RefreshToken)
        .where(RefreshToken.family_id == family_id)
        .with_for_update()
    ).all()

    for record in records:
        if record.revoked_at is None:
            record.revoked_at = now


def unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
    )


@app.get("/")
def home():
    return {"message": "Authentication + PostgreSQL integration"}


@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    existing_user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="user",
        is_active=True,
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from None

    return user


@app.post("/token", response_model=TokenResponse)
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    # The OAuth2 "username" field contains the user's email.
    user = db.scalar(
        select(User).where(User.email == form_data.username)
    )

    if user is None or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    # A new login creates a new token family.
    family_id = secrets.token_urlsafe(24)

    raw_refresh_token, refresh_record = create_refresh_record(
        user_id=user.id,
        family_id=family_id,
    )

    db.add(refresh_record)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": raw_refresh_token,
        "token_type": "bearer",
    }


@app.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    request: RefreshRequest,
    db: Annotated[Session, Depends(get_db)],
):
    now = datetime.now(timezone.utc)
    incoming_hash = hash_refresh_token(request.refresh_token)

    # Lock the matching token row while processing rotation.
    old_token = db.scalar(
        select(RefreshToken)
        .where(RefreshToken.token_hash == incoming_hash)
        .with_for_update()
    )

    if old_token is None:
        raise unauthorized()

    # A previously revoked token is being reused.
    if old_token.revoked_at is not None:
        revoke_token_family(db, old_token.family_id, now)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token reuse detected; login required",
        )

    # Expired tokens cannot be refreshed.
    if old_token.expires_at <= now:
        revoke_token_family(db, old_token.family_id, now)
        db.commit()
        raise unauthorized()

    user = db.get(User, old_token.user_id)

    if user is None or not user.is_active:
        revoke_token_family(db, old_token.family_id, now)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is unavailable",
        )

    # Revoke the old token and create a replacement in the same family.
    raw_new_refresh_token, new_record = create_refresh_record(
        user_id=user.id,
        family_id=old_token.family_id,
    )

    old_token.revoked_at = now
    old_token.replaced_by_hash = new_record.token_hash

    db.add(new_record)

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": raw_new_refresh_token,
        "token_type": "bearer",
    }


@app.post("/logout")
def logout(
    request: RefreshRequest,
    db: Annotated[Session, Depends(get_db)],
):
    now = datetime.now(timezone.utc)
    incoming_hash = hash_refresh_token(request.refresh_token)

    token_record = db.scalar(
        select(RefreshToken)
        .where(RefreshToken.token_hash == incoming_hash)
    )

    if token_record is not None:
        revoke_token_family(db, token_record.family_id, now)
        db.commit()

    # Return the same response even if the supplied token is unknown.
    return {"message": "Logged out"}


@app.get("/users/me", response_model=UserResponse)
def read_current_user(current_user: CurrentUser):
    return current_user


@app.get("/admin", response_model=UserResponse)
def admin_dashboard(current_user: AdminUser):
    return current_user

@app.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.scalar(
        select(User).where(User.email == request.email)
    )

    # Same response for existing and non-existing emails
    # helps prevent account enumeration.
    response = {
        "message": (
            "If the account exists, password reset instructions "
            "will be provided."
        )
    }

    if user is None or not user.is_active:
        return response

    now = datetime.now(timezone.utc)

    # Invalidate earlier unused reset tokens for this user.
    old_tokens = db.scalars(
        select(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
        .with_for_update()
    ).all()

    for old_token in old_tokens:
        old_token.used_at = now

    raw_token = generate_refresh_token()

    reset_record = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_refresh_token(raw_token),
        expires_at=now + timedelta(
            minutes=settings.password_reset_expire_minutes
        ),
    )

    db.add(reset_record)
    db.commit()

    # DEVELOPMENT ONLY: do not return reset tokens in production.
    # A real application should send a reset link by email.
    response["development_reset_token"] = raw_token

    return response


@app.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Annotated[Session, Depends(get_db)],
):
    now = datetime.now(timezone.utc)
    token_hash = hash_refresh_token(request.token)

    reset_record = db.scalar(
        select(PasswordResetToken)
        .where(PasswordResetToken.token_hash == token_hash)
        .with_for_update()
    )

    if reset_record is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    if reset_record.used_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    if reset_record.expires_at <= now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    user = db.get(User, reset_record.user_id)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to reset password",
        )

    # Save the new password as an Argon2 hash.
    user.hashed_password = hash_password(request.new_password)
    reset_record.used_at = now

    # Invalidate all refresh-token sessions for this user.
    refresh_records = db.scalars(
        select(RefreshToken)
        .where(
            RefreshToken.user_id == user.id,
            RefreshToken.revoked_at.is_(None),
        )
        .with_for_update()
    ).all()

    for refresh_record in refresh_records:
        refresh_record.revoked_at = now

    # Invalidate any other unused reset tokens for this user.
    other_reset_tokens = db.scalars(
        select(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.id != reset_record.id,
            PasswordResetToken.used_at.is_(None),
        )
        .with_for_update()
    ).all()

    for other_token in other_reset_tokens:
        other_token.used_at = now

    db.commit()

    return {
        "message": (
            "Password reset successful. Please log in with your new password."
        )
    }