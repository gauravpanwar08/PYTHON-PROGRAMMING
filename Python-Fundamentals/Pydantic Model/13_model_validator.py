# ============================================================
#             PYDANTIC - MODEL VALIDATOR
# model_validator() → Validates the entire model OR multiple fields at once whose validation/relationship depends on each other
#
# mode="before"          → Runs before Pydantic validates the fields
# mode="after"           → Runs after Pydantic validates the fields
# Cross-field Validation → Validates relationships between multiple fields
# Model Transformation   → Can modify model data after validation
# =========================================================================

from typing import Any

from pydantic import BaseModel, model_validator


class User(BaseModel):

    name: str
    age: int
    password: str
    confirm_password: str

    # --------------------------------------------------------
    # mode="before"
    # --------------------------------------------------------

    @model_validator(mode="before")
    @classmethod
    def clean_input(cls, data: Any):

        print("\nBefore Model Validation:")
        print("Data:", data)

        if isinstance(data, dict):

            if isinstance(data.get("name"), str):
                data["name"] = data["name"].strip()

        return data

    # --------------------------------------------------------
    # mode="after"
    # --------------------------------------------------------

    @model_validator(mode="after")
    def validate_user(self):

        print("\nAfter Model Validation:")
        print("User:", self)

        if self.age < 18:
            raise ValueError(
                "User must be 18 or above"
            )

        return self

    # --------------------------------------------------------
    # Cross-field Validation
    # --------------------------------------------------------

    @model_validator(mode="after")
    def validate_passwords(self):

        if self.password != self.confirm_password:
            raise ValueError(
                "Password and confirm password must match"
            )

        return self


# Create User

user = User(
    name="   Gaurav   ",
    age=22,
    password="secret123",
    confirm_password="secret123"
)


# Print User

print("\nUser:")
print(user)

print("\nDictionary:")
print(user.model_dump())