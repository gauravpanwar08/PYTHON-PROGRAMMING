# ============================================================
#             PYDANTIC - PYTHON TYPES & VALIDATION
# ============================================================

from pydantic import BaseModel


# User Model

class User(BaseModel):
    name: str
    age: int
    is_active: bool
    height: float


# Create Valid Data

user = User(
    name="Gaurav",
    age=22,
    is_active=True,
    height=5.9
)

# # Create Invalid Data

# user = User(
#     name="Gaurav",
#     age="hello",    # It will raise a validation error because age should be an integer
#     is_active=True,
#     height=5.9
# )

# Access Data

print(user)

print("Name:", user.name)
print("Age:", user.age)
print("Active:", user.is_active)
print("Height:", user.height)