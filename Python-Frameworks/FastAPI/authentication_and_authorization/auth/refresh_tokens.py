
import hashlib
import secrets


def generate_refresh_token() -> str:
    # Cryptographically secure, unpredictable token.
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    # SHA-256 is suitable here because refresh tokens are
    # randomly generated high-entropy secrets, not user passwords.
    return hashlib.sha256(token.encode("utf-8")).hexdigest()