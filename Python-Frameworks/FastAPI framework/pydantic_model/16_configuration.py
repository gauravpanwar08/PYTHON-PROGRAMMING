# ============================================================================================
# PYDANTIC - ConfigDict : used to configure the behavior of Pydantic models
#
# ConfigDict options:
#            1. a. extra="forbid"           - prevent extra fields in the model
#               b. extra="allow"            - allow extra fields in the model
#               c. extra="ignore"           - ignore extra fields in the model
#            2. str_strip_whitespace=True   - Remove leading/trailing whitespace from strings
#            3. validate_assignment=True    - Validate values when they are assigned
#            4. frozen=True                 - Make the model immutable
# ============================================================================================


from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI()

# USER MODEL

class User(BaseModel):

    model_config = ConfigDict(

        # Extra fields are not allowed
        # ----------------------------------------------------
        extra="forbid",

        # Remove leading/trailing whitespace
        # ----------------------------------------------------
        str_strip_whitespace=True,

        # Validate values when they are assigned
        # ----------------------------------------------------
        validate_assignment=True,

        # Make the model immutable
        # ----------------------------------------------------
        frozen=True
    )

    name: str
    age: int
    email: str


# CREATE USER

@app.post("/users")
def create_user(user: User):

    print("User:")
    print(user)

    print("\nName:")
    print(user.name)

    print("\nAge:")
    print(user.age)

    print("\nEmail:")
    print(user.email)

    return {
        "message": "User created successfully",
        "user": user.model_dump()
    }


# GET USER

@app.get("/users")
def get_user():

    user = User(
        name="  Gaurav  ",
        age=22,
        email="  gaurav@example.com  "
    )

    return {
        "user": user.model_dump()
    }



# TEST FROZEN MODEL
# frozen=True means fields cannot be modified after the Pydantic model has been created.

@app.put("/users/test-update")
def test_update():

    user = User(
        name="Gaurav",
        age=22,
        email="gaurav@example.com"
    )

    try:

        # This will fail because frozen=True

        user.age = 23

        return {
            "message": "Age updated",
            "user": user.model_dump()
        }

    except Exception as error:

        return {
            "message": "User cannot be modified",
            "error": str(error)
        }

