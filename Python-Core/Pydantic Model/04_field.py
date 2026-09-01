# ============================================================
#       PYDANTIC - FIELD() & FIELD CONSTRAINTS
# ============================================================


from pydantic import BaseModel, Field


class User(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=50,
        description="User's full name"
    )

    age: int = Field(
        ge=18,
        le=100,
        description="User age must be between 18 and 100"
    )

    username: str = Field(
        min_length=3,
        max_length=20,
        description="Unique username"
    )

    is_active: bool = Field(
        default=True,
        description="Whether the user account is active"
)

    email: str

user = User(
    name="Gaurav",
    age=22,
    email="gaurav@example.com",
    username="gaurav123"
)

print(user)
print(user.name)
print(user.age)
print(user.username)
print(user.is_active)
