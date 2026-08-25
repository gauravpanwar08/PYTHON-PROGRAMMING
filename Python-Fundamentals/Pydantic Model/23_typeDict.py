# ============================================================
#          PYTHON TYPING - TypedDict
#
# TypedDict     → Defines the expected structure of a dictionary
# total=False   → Makes all fields optional by default
# Required      → Makes a field required
# NotRequired   → Makes a field optional
#
# Important → TypedDict does NOT perform runtime validation.
# ============================================================


from typing import NotRequired, Required, TypedDict

# ------------------------------------------------------------
# TypedDict with Required and NotRequired
# ------------------------------------------------------------

class User(TypedDict):

    # Required fields
    name: Required[str]
    age: Required[int]
    email: Required[str]

    # Optional field
    phone: NotRequired[str]


# Create User

user: User = {"name": "Gaurav", "age": 22, "email": "gaurav@example.com"}


# Print User

print("User:")
print(user)


# ------------------------------------------------------------
# Access User Data
# ------------------------------------------------------------

print("\nName:")
print(user["name"])

print("\nAge:")
print(user["age"])

print("\nEmail:")
print(user["email"])


# ------------------------------------------------------------
# total=False
# ------------------------------------------------------------


class UserUpdate(TypedDict, total=False):

    name: str
    age: int
    email: str
    phone: str


# Only one field can be provided

update_data: UserUpdate = {"age": 23}

print("\nUser Update:")
print(update_data)


# ------------------------------------------------------------
# total=False + Required
# ------------------------------------------------------------


class UserUpdateRequired(TypedDict, total=False):

    # Required even though total=False
    user_id: Required[int]

    # Optional because of total=False
    name: str
    age: int
    email: str


update: UserUpdateRequired = {"user_id": 1, "age": 23}

print("\nUser Update Required:")
print(update)


# ------------------------------------------------------------
# Required + NotRequired
# ------------------------------------------------------------


class Product(TypedDict):

    id: Required[int]
    name: Required[str]

    # Optional
    description: NotRequired[str]
    price: NotRequired[float]


product: Product = {"id": 101, "name": "Laptop"}

print("\nProduct:")
print(product)
