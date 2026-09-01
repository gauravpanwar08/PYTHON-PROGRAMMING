# ============================================================
#                 PYDANTIC - BaseModel
# ============================================================
# Pydantic is a fast and popular data validation and parsing library for Python.
#  It uses standard Python type hints to check, convert, and ensure that data matches the expected structure before program uses it.
# ----------------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel    # BaseModel is the core class and basic building block of Pydantic.

app = FastAPI()

class User(BaseModel):
    name : str
    age : int
    email : str
    
@app.post("/users")
def create_user(user: User):
    return {
        "received_user_data": user,
        "message": "User created successfully"
    }
    