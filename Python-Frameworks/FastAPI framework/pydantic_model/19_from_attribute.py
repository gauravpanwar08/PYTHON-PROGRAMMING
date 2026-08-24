# ===========================================================================
#             PYDANTIC - from_attributes=True
#
# from_attributes=True → Allows Pydantic to read data or create response model
#                     from object attributes instead of requiring a dictionary.
# Main Use → Converting ORM objects into Pydantic models.
# ===========================================================================


from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict


app = FastAPI()


# Fake ORM Object
# Later this will be replaced by a SQLAlchemy model

class UserORM:

    def __init__(
        self,
        id: int,
        name: str,
        age: int,
        email: str
    ):
        self.id = id
        self.name = name
        self.age = age
        self.email = email


# Pydantic Response Model

class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    age: int
    email: str


# Get User

@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(user_id: int):

    # Normally this object would come from SQLAlchemy

    user = UserORM(
        id=user_id,
        name="Gaurav",
        age=22,
        email="gaurav@example.com"
    )

    return user
