# ====================================================================
#                 PYTHON TYPING - TypeAlias
#
# TypeAlias → Gives a meaningful name to an existing type.
# Main Use → Makes complex/repeated type annotations reusable/readable
# =====================================================================


from typing import TypeAlias

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ------------------------------------------------------------
# Type Aliases
# ------------------------------------------------------------

UserID: TypeAlias = int

Skills: TypeAlias = list[str]


# User Model

class User(BaseModel):

    id: UserID
    name: str
    skills: Skills


# ------------------------------------------------------------
# Create User
# ------------------------------------------------------------

@app.post("/users")
def create_user(user: User):

    return {
        "message": "User created successfully",
        "user": user
    }


# ------------------------------------------------------------
# Get User
# ------------------------------------------------------------

@app.get(
    "/users/{user_id}",
    response_model=User
)
def get_user(user_id: UserID):

    return User(
        id=user_id,
        name="Gaurav",
        skills=[
            "Python",
            "FastAPI",
            "Pydantic"
        ]
    )
