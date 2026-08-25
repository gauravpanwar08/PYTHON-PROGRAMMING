# ============================================================
#       PYDANTIC - ValidationError
#
# Methods covered:
#                1. ValidationError
#                2. errors()
#                3. error_count()
#                4. json()
# ============================================================


from pydantic import BaseModel, ValidationError

# USER MODEL


class User(BaseModel):

    name: str
    age: int
    email: str


# INVALID USER

try:

    user = User(name="Gaurav", age="hello", email="gaurav@example.com")

except ValidationError as error:

    # --------------------------------------------------------
    # Complete error
    # --------------------------------------------------------

    print("VALIDATION ERROR:")
    print(error)

    # --------------------------------------------------------
    # 1. errors()
    # --------------------------------------------------------

    print("\n1. errors()")
    print(error.errors())

    # --------------------------------------------------------
    # 2. error_count()
    # --------------------------------------------------------

    print("\n2. error_count()")
    print(error.error_count())

    # --------------------------------------------------------
    # 3. json()
    # --------------------------------------------------------

    print("\n3. json()")
    print(error.json())

    # Access first error

    first_error = error.errors()[0]

    print("\n4. First Error:")
    print(first_error)

    # Error location

    print("\nError Location:")
    print(first_error["loc"])

    # Error message

    print("\nError Message:")
    print(first_error["msg"])

    # Error type

    print("\nError Type:")
    print(first_error["type"])
