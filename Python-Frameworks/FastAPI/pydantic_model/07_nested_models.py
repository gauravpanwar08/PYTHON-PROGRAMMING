# ============================================================
#              PYDANTIC - NESTED MODELS
# A Pydantic model can contain another Pydantic model.
#
# Example:
#
# User
# ├── name
# ├── age
# └── address
#       ├── city
#       ├── state
#       └── pincode
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# Address Model


class Address(BaseModel):
    city: str
    state: str
    pincode: int


# User Model


class User(BaseModel):
    name: str
    age: int
    email: str
    address: Address


# Create User

user = User(
    name="Gaurav",
    age=22,
    email="gaurav@example.com",
    address=Address(city="Dehradun", state="Uttarakhand", pincode=248001),
)

# Create User Endpoint


@app.post("/users")
def create_user(user: User):
    return user
