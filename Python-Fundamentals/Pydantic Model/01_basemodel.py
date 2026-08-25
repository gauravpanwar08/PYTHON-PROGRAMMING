# ============================================================
#                 PYDANTIC - BaseModel
# ============================================================
# Pydantic is a fast and popular data validation and parsing library for Python.
# BaseModel is the core class and basic building block of Pydantic.

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str


user = User(
    name="Gaurav",
    age=22,
    email="gaurav@example.com"
)

print(user)

print(user.name)
print(user.age)
print(user.email)

print(user.model_dump())       # This will print the dictionary representation of the user object
print(user.model_dump_json())  # This will print the JSON representation of the user object