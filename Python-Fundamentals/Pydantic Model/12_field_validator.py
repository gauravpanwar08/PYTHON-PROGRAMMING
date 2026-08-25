# ==================================================
#          PYDANTIC - FIELD VALIDATOR
#
# field_validator()    → Validates a specific field
# mode="before"        → Runs before Validation/type conversion or works on the raw input value
# mode="after"         → Runs after Validation/type conversion or works on the validated/parsed value and it is the default mode
# ValidationInfo       → Provides information about the current field and already validated data
# Value Transformation → Modifies/cleans the input value
# Error Detection      → Checks custom conditions and raises ValueError when validation fails
# ================================================================================================================================


from typing import Any
from pydantic import BaseModel, ValidationInfo, field_validator


class User(BaseModel):
    name: str
    username: str
    age: int
    email: str
    
    # ----------------------------------------------------------------------
    # Error Detection - Validator can also be used to check/detect the error
    #-----------------------------------------------------------------------

    @field_validator("username")  # validate single field username
    @classmethod
    def check_space(cls, value):

        if " " in value:  # check if there is a space in the username
            raise ValueError("Username cannot contain spaces")
        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Age must be 18 or above")
        return value
    
    @field_validator("name", "username")   # validate multiple fields individually
    @classmethod
    def validate_text(cls, value):
        return value
    
    
    # --------------------------------------------------------
    # mode="before"
    # --------------------------------------------------------

    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, value: Any):

        print("\nBefore Validation:")
        print("Value:", value)
        print("Type:", type(value))

        if isinstance(value, str):
            return value.strip()     # Remove leading/trailing whitespace before validation

        return value
    
    
    # --------------------------------------------------------
    # mode="after"
    # --------------------------------------------------------

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, value: str):

        print("\nAfter Validation:")
        print("Value:", value)
        print("Type:", type(value))

        if len(value) < 3:
            raise ValueError(
                "Name must contain at least 3 characters"
            )

        return value
    
    
    # ----------------------------------------------------------------------
    # Value Transformation - Validator can also be used to modify the value
    #-----------------------------------------------------------------------

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        return value.strip().lower()  # Remove whitespace and convert username to lowercase

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        return value.title()      # Convert name to title case
    
    
    # --------------------------------------------------------
    # ValidationInfo
    # --------------------------------------------------------

    @field_validator("email")
    @classmethod
    def validate_email(
        cls,
        value: str,
        info: ValidationInfo
    ):

        print("\nValidationInfo:")
        print("Field:", info.field_name)
        print("Already validated data:", info.data)

        if not value.endswith("@example.com"):
            raise ValueError(
                "Email must end with @example.com"
            )

        return value

# Create an instance of the User model

user = User(
    name="gaurav Panwar  ",
    username="GAURAV08",
    age=22,
    email="gaurav@example.com"
)

print("\nUser:")
print(user)