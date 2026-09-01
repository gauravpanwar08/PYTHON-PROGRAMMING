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

from pydantic import BaseModel


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


print("User Details:")
print(user)


# Access Nested Data

print("\nUser Name:")
print(user.name)

print("\nCity:")
print(user.address.city)

print("\nState:")
print(user.address.state)

print("\nPincode:")
print(user.address.pincode)
