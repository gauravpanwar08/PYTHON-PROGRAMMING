# ===========================================================================
#             PYDANTIC - from_attributes=True
#
# from_attributes=True → Allows Pydantic to read data from object attributes 
#                        instead of requiring a dictionary.
# Main Use → Converting ORM objects into Pydantic models.
# ===========================================================================

from pydantic import BaseModel, ConfigDict


# Normal Python Object

class UserObject:

    def __init__(
        self,
        name: str,
        age: int,
        email: str
    ):
        self.name = name
        self.age = age
        self.email = email


# Pydantic Response Model

class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    name: str
    age: int
    email: str


# Create Normal Python Object

user_object = UserObject(
    name="Gaurav",
    age=22,
    email="gaurav@example.com"
)


# Convert Object to Pydantic Model

user = UserResponse.model_validate(
    user_object
)


# Print Pydantic Model

print("Pydantic User:")
print(user)


# Convert to Dictionary

print("\nDictionary:")
print(user.model_dump())
