# Extracts the Bearer token, validates its JWT claims,
# and retrieves the corresponding active demo user.

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from auth.token import decode_access_token
from db.dependencies import get_db
from models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
    except InvalidTokenError:
        raise credentials_exception from None

    subject = payload.get("sub")

    if not isinstance(subject, str) or not subject.isdigit():
        raise credentials_exception

    user = db.get(User, int(subject))

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
