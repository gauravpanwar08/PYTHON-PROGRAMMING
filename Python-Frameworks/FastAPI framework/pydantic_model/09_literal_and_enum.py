# ============================================================
#       PYDANTIC - RESTRICTED VALUES - Literal & Enum
#
# Both are used to restrict the values of a field to a specific set of allowed values as a constraint in pydantic models.
# Literal → Allowed directly fixed values
# Enum → Allowed reusable group of fixed values
# ============================================================

from enum import Enum
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# User Role Enum

class UserRole(str, Enum):            # Enum class for user roles
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


# User Model

class User(BaseModel):
    name: str

    # Literal
    status: Literal["active", "inactive"]    # Literal type for user status

    # Enum
    role: UserRole


# Create User Endpoint

@app.post("/users")
def create_user(user: User):

    print("User:")
    print(user)

    print("\nStatus:")
    print(user.status)

    print("\nRole:")
    print(user.role)

    print("\nRole Value:")
    print(user.role.value)

    return user

