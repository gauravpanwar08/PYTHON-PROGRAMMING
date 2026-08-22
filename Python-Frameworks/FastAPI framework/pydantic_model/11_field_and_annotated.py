# ============================================================
# PYDANTIC -> NORMAL Field() vs Annotated + Field()
# Both approaches perform the same type of validation.
#
# Normal Field Format-
#     name: str = Field(min_length=3)
#
# Annotated Format-
#     name: Annotated[str, Field(min_length=3)]
# ============================================================

from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel, Field


app= FastAPI()


# NORMAL Field()
# -------------------------------------------

class UserNormal(BaseModel):

    # Type + Field directly on the field
    name: str = Field(
        min_length=3,
        max_length=50
    )

    age: int = Field(
        ge=18,
        le=100
    )

    username: str = Field(
        min_length=3,
        max_length=20
    )


# Annotated + Field()
# ----------------------------------------------------

class UserAnnotated(BaseModel):

    # Type and validation metadata are separated
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50
        )
    ]

    age: Annotated[
        int,
        Field(
            ge=18,
            le=100
        )
    ]

    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=20
        )
    ]


# NORMAL Field() ENDPOINT

@app.post("/users/normal")
def create_user_normal(user: UserNormal):

    print("\nNORMAL Field() User:")
    print(user)

    return {
        "message": "User created using Normal Field()",
        "user": user.model_dump()
    }


# ANNOTATED + Field() ENDPOINT

@app.post("/users/annotated")
def create_user_annotated(user: UserAnnotated):

    print("\nANNOTATED + Field() User:")
    print(user)

    return {
        "message": "User created using Annotated + Field()",
        "user": user.model_dump()
    }
    