# ============================================================
#          PYDANTIC - FIELD VALIDATOR
# field_validator() → Validates a specific field
#
# mode="before" → Before Validation/type conversion
# mode="after"  → After Validation/type conversion
#                  and it is the default mode
# ============================================================


from fastapi import FastAPI
from pydantic import BaseModel, field_validator


app = FastAPI()

# PYDANTIC MODEL

class User(BaseModel):

    name: str
    username: str
    age: int


    # FIELD VALIDATOR

    @field_validator("username")
    @classmethod
    def check_space(cls, value):

        if " " in value:

            raise ValueError(
                "Username cannot contain spaces"
            )

        return value


    # VALIDATOR CAN ALSO MODIFY THE VALUE

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):

        return value.strip().lower()


    @field_validator("name")
    @classmethod
    def validate_name(cls, value):

        return value.title()


    @field_validator("age")
    @classmethod
    def validate_age(cls, value):

        if value < 18:

            raise ValueError(
                "Age must be 18 or above"
            )

        return value


    # VALIDATE MULTIPLE FIELDS INDIVIDUALLY

    @field_validator("name", "username")
    @classmethod
    def validate_text(cls, value):

        return value


    # mode="before" - Runs before Pydantic validation/type conversion

    @field_validator("name", mode="before")
    @classmethod
    def validate_name_before(cls, value):

        return value.strip()


    # mode="after" - Runs after Pydantic validation/type conversion
    #"after" is the default mode

    @field_validator("username", mode="after")
    @classmethod
    def validate_username_after(cls, value):

        return value


# FASTAPI ENDPOINT

@app.post("/users")
def create_user(user: User):

    return {
        "message": "User created successfully",
        "user": user
    }
