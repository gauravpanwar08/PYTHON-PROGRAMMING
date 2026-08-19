# ===============================================================
# PYDANTIC - REQUIRED FIELDS & DEFAULT VALUES & OPTIONAL FIELDS
# ===============================================================

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

@app.post("/users")
def create_user(user: User):
        return user
