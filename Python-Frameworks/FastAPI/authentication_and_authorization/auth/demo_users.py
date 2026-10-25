
# Stores demo users in memory to demonstrate role-based authorization.
# Production applications should load users and roles from a database.

from auth.password_hashing import hash_password

DEMO_USERS = {
    "demo@example.com": {
        "id": "101",
        "username": "demo@example.com",
        "hashed_password": hash_password("demo123"),
        "role": "user",
        "is_active": True,
    },
    "admin@example.com": {
        "id": "102",
        "username": "admin@example.com",
        "hashed_password": hash_password("admin123"),
        "role": "admin",
        "is_active": True,
    },
}


def get_demo_user_by_username(username: str) -> dict | None:
    return DEMO_USERS.get(username)


def get_demo_user_by_id(user_id: str) -> dict | None:
    for user in DEMO_USERS.values():
        if user["id"] == user_id:
            return user
    return None
