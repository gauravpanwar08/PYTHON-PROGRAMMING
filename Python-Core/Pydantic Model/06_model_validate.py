# ============================================================
#               PYDANTIC - model_validate()
#
# model_validate() is used to validate data and create a Pydantic model instance from that data.
# Common use:  Dictionary / external data --> model_validate() --> Pydantic Model
# =================================================================

from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    email: str


# Dictionary Data

user_data = {
    "name": "Gaurav",
    "age": 22,
    "email": "gaurav@example.com"
}


# Validate Dictionary and Create Pydantic Model
# Dictionary → Pydantic Model

user = User.model_validate(user_data)

print("Pydantic Object:")
print(user)

print("\nType:")
print(type(user))


print("\nUser Name:")
print(user.name)

print("\nUser Age:")
print(user.age)

print("\nUser Email:")
print(user.email)