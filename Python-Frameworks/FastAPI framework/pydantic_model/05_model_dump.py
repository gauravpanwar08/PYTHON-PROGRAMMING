# ============================================================
#               FASTAPI + PYDANTIC - model_dump()
#
# model_dump() is a method that converts a Pydantic model instance into a dictionary representation.
# In FastAPI, this is useful when we want to process, filter, or customize the data before returning a response.
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
    city: str | None = None
    password: str


# Create User

@app.post("/users")
def create_user(user: User):

   # Pydantic Model before converting to Dictionary

    print("Pydantic Object:")
    print(user)


    # Convert Pydantic Model to Dictionary

    user_data = user.model_dump()

    print("\nDictionary:")
    print(user_data)

    print("\nType:")
    print(type(user_data))


    # 1. Exclude Specific Fields
    # ------------------------------------------------------------

    print("\n1. EXCLUDE FIELDS")

    user_without_password = user.model_dump(
        exclude={"password"}
    )

    print(user_without_password)


    # 2. Include Specific Fields
    # ------------------------------------------------------------

    print("\n2. INCLUDE FIELDS")

    user_basic_info = user.model_dump(
        include={"name", "email"}
    )

    print(user_basic_info)


    # 3. Exclude None Values
    # ------------------------------------------------------------

    print("\n3. EXCLUDE NONE")

    user_without_none = user.model_dump(
        exclude_none=True
    )

    print(user_without_none)


    # Return Response

    return {
        "user_data": user_data,
        "without_password": user_without_password,
        "basic_info": user_basic_info,
        "without_none": user_without_none
    }