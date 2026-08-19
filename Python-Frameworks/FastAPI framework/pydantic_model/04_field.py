# ============================================================
#          PYDANTIC - FIELD() & FIELD CONSTRAINTS
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


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


@app.post("/users")
def create_user(user: User):
    return user
