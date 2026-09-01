# ===============================================================
# PYDANTIC - REQUIRED FIELDS & DEFAULT VALUES & OPTIONAL FIELDS
# ===============================================================

from pydantic import BaseModel

# 1. Required Fields

class User(BaseModel):
    name: str                   # Required field
    age: int                    # Required field
    is_active: bool = True      # Default Values
    contact: str | None = None  # Optional field


user1 = User(
    name="Gaurav",
    age=22
)

user2 = User(
    name="Rahul",
    age=25,
    contact="987654xxxx",
    is_active=False
)

print(user1)
print(user2)