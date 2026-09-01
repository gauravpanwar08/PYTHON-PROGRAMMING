# ============================================================
#             PYDANTIC - PYTHON TYPES & VALIDATION
# ============================================================


from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# User Request Model

class User(BaseModel):
    name: str
    age: int
    is_active: bool
    height: float


# Create User Endpoint

@app.post("/users")
def create_user(user: User):
    return user