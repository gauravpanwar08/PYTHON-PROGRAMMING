# ============================================================
#          FASTAPI + PYDANTIC - ADVANCED model_dump()
#
# model_dump()           → Converts a Pydantic model into a dictionary
# exclude_none=True      → Excludes fields whose value is None
# exclude_unset=True     → Excludes fields that were not explicitly provided
# exclude_defaults=True  → Excludes fields having their default value
# include={}             → Includes only selected fields
# exclude={}             → Excludes selected fields
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# User Model

class User(BaseModel):

    name: str
    age: int
    email: str
    phone: str | None = None
    is_active: bool = True


# Update User Model

class UserUpdate(BaseModel):

    name: str | None = None
    age: int | None = None
    email: str | None = None
    phone: str | None = None
    is_active: bool = True


# Create User

@app.post("/users")
def create_user(user: User):

    return {
        "user": user.model_dump()
    }


# Get User without None values

@app.get("/users/{user_id}")
def get_user(user_id: int):

    user = User(
        name="Gaurav",
        age=22,
        email="gaurav@example.com"
    )

    return user.model_dump(
        exclude_none=True
    )


# Update User

@app.patch("/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdate
):

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    return {
        "user_id": user_id,
        "updated_fields": update_data
    }


# Return fields without their default values

@app.get("/users/{user_id}/without-defaults")
def get_user_without_defaults(user_id: int):

    user = User(
        name="Gaurav",
        age=22,
        email="gaurav@example.com"
    )

    return user.model_dump(
        exclude_defaults=True
    )


# Return only selected fields

@app.get("/users/{user_id}/basic")
def get_basic_user(user_id: int):

    user = User(
        name="Gaurav",
        age=22,
        email="gaurav@example.com"
    )

    return user.model_dump(
        include={
            "name",
            "email"
        }
    )


# Exclude selected fields

@app.get("/users/{user_id}/safe")
def get_safe_user(user_id: int):

    user = User(
        name="Gaurav",
        age=22,
        email="gaurav@example.com"
    )

    return user.model_dump(
        exclude={
            "email"
        }
    )
