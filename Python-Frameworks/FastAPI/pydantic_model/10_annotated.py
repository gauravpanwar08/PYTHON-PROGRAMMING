# ===============================================================================================
#                FASTAPI + PYDANTIC - ANNOTATED + FIELD()
# It is used to add metadata and validation constraints to the fields of a Pydantic model.
# It is same as using Field() directly but it is a modern approach that allows more readable code.
# Format: Annotated[type, Field(...)]
# ================================================================================================

from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


# USER MODEL

class User(BaseModel):

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            description="User's full name"
        )
    ]

    age: Annotated[
        int,
        Field(
            ge=18,
            le=100,
            description="User age"
        )
    ]

    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=20,
            description="Unique username"
        )
    ]

# CREATE USER

@app.post("/users")
def create_user(user: User):

    return user
