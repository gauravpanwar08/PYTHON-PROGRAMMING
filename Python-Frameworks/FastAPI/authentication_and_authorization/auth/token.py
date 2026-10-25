
# Create and verify signed JWT access tokens with expiration.

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

from core.config import settings


# ------------------
# JWT Configuration
# ------------------
# Use a fixed, explicitly configured signing algorithm.

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
SECRET_KEY = settings.jwt_secret_key


# ------------------
# Create Access Token
# ------------------
# Sign claims and attach an expiration timestamp.

def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_token


# ------------------
# Decode Access Token
# ------------------
# Verify signature and required claims, including expiration.

def decode_access_token(token: str) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"require": ["exp", "sub"]},
    )

    return payload
