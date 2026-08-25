# ============================================================
#       PYDANTIC - RESTRICTED VALUES - Literal & Enum
#
# Both are used to restrict the values of a field to a specific set of allowed values as a constraint in pydantic models.
# Literal → Allowed directly fixed values
# Enum → Allowed reusable group of fixed values
# ============================================================

from enum import Enum
from typing import Literal

from pydantic import BaseModel



class UserRole(str, Enum):         # enum -----
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


# USER MODEL

class User(BaseModel):
    name: str
    status: Literal["active", "inactive"]    # literal ----
    role: UserRole                           # enum -----


# CREATE USER

user = User(
    name="Gaurav",
    status="active",
    role="admin"
)


# PRINT USER

print("User:")
print(user)


# ACCESS LITERAL VALUE
# ---------------------

print("\nStatus:")
print(user.status)


# ACCESS ENUM
# ------------

print("\nRole:")
print(user.role)


# ACCESS ENUM VALUE
# ---------------------

print("\nRole Value:")
print(user.role.value)


# MODEL DUMP

print("\nDictionary:")
print(user.model_dump())

