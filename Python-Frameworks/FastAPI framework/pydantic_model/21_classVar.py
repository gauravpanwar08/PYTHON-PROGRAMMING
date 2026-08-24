# ========================================================================================================
#               PYDANTIC - ClassVar
#
# ClassVar → Class-level variable that is not treated as a Pydantic request/response field.
#
# Main Use → Constants, shared class-level configuration, counters or metadata that should not be model data.
# ===========================================================================================================

from typing import ClassVar

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# User Model

class User(BaseModel):

    name: str
    age: int

    # Class variable
    company: ClassVar[str] = "ABC Technologies"


# Create User Endpoint

@app.post("/users")
def create_user(user: User):

    return {
        "user": user.model_dump(),
        "company": User.company
    }


# Get Company

@app.get("/company")
def get_company():

    return {
        "company": User.company
    }
