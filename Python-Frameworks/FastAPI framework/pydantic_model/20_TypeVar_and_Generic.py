# ============================================================================================
#              PYTHON TYPING - TypeVar + Generic
#
# TypeVar  → Creates a reusable type variable that can represent different types
#            while preserving type information
#
# Generic  → Allows the same class/function/model structure to work with different data types
#            and type variable in a reusable way.
#
# Main Use → Reusable typed classes, functions and Pydantic models
# =============================================================================================


from typing import Generic, TypeVar

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


T = TypeVar("T")


# Generic Response Model

class Response(BaseModel, Generic[T]):

    success: bool
    data: T


# User Model

class User(BaseModel):

    id: int
    name: str
    email: str


# ------------------------------------------------------------
# Generic Response with User
# ------------------------------------------------------------

@app.get(
    "/user",
    response_model=Response[User]
)
def get_user():

    user = User(
        id=1,
        name="Gaurav",
        email="gaurav@example.com"
    )

    return Response[User](
        success=True,
        data=user
    )


# ------------------------------------------------------------
# Generic Response with List[User]
# ------------------------------------------------------------

@app.get(
    "/users",
    response_model=Response[list[User]]
)
def get_users():

    users = [
        User(
            id=1,
            name="Gaurav",
            email="gaurav@example.com"
        ),
        User(
            id=2,
            name="Rahul",
            email="rahul@example.com"
        )
    ]

    return Response[list[User]](
        success=True,
        data=users
    )


# ------------------------------------------------------------
# Generic Response with String
# ------------------------------------------------------------

@app.get(
    "/message",
    response_model=Response[str]
)
def get_message():

    return Response[str](
        success=True,
        data="User created successfully"
    )
