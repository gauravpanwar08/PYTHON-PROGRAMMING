# ==========================================================================================================
#                    PYTHON - ClassVar
#
# ClassVar → Declares a class-level variable that should not be treated as an instance/model field.
#
# Main Use → Constants, shared class-level configuration, counters or metadata that should not be model data.
# ===========================================================================================================

from typing import ClassVar

from pydantic import BaseModel


# User Model

class User(BaseModel):

    name: str
    age: int

    # Class variable
    company: ClassVar[str] = "ABC Technologies"


# Create User

user = User(
    name="Gaurav",
    age=22
)


# Print User

print("User:")
print(user)


# Access ClassVar

print("\nCompany:")
print(User.company)

print(user.company)


# Model Dump

print("\nmodel_dump():")
print(user.model_dump())


# Model Fields

print("\nModel Fields:")
print(User.model_fields)
