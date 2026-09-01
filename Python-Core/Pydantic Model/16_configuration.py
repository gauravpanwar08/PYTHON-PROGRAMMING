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


from pydantic import BaseModel, ConfigDict

# USER MODEL

class User(BaseModel):

    model_config = ConfigDict(
       
        # Extra fields are not allowed
        # ----------------------------------------------------
        extra="forbid",

        # Remove leading/trailing whitespace from strings
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

user = User(
    name="  Gaurav  ",
    age=22,
    email="  gaurav@example.com  "
)


# PRINT USER

print("User:")
print(user)


# CHECK STRIP WHITESPACE

print("\nName:")
print(user.name)

print("\nEmail:")
print(user.email)


# TRY TO MODIFY USER - frozen=True means the model cannot be modified.

try:

    user.age = 23

except Exception as error:

    print("\nAssignment Error:")
    print(error)