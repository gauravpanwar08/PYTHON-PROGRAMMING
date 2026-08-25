# ============================================================
#              PYDANTIC - ADVANCED model_dump()
#
# model_dump()          → Converts a Pydantic model into a dictionary
# exclude_none=True     → Excludes fields whose value is None
# exclude_unset=True   → Excludes fields that were not explicitly provided
# exclude_defaults=True → Excludes fields having their default value
# include={}            → Includes only selected fields
# exclude={}            → Excludes selected fields
# Nested include/exclude → Controls fields inside nested models
# ============================================================

from pydantic import BaseModel


# Address Model

class Address(BaseModel):

    city: str
    state: str
    country: str = "India"


# User Model

class User(BaseModel):

    name: str
    age: int
    email: str
    phone: str | None = None
    is_active: bool = True
    address: Address


# Create User

user = User(
    name="Gaurav",
    age=22,
    email="gaurav@example.com",
    address={
        "city": "Dehradun",
        "state": "Uttarakhand"
    }
)


# Basic model_dump()

print("Basic model_dump():")
print(user.model_dump())


# ------------------------------------------------------------
# exclude_none=True
# ------------------------------------------------------------

print("\nexclude_none=True:")

print(
    user.model_dump(
        exclude_none=True
    )
)


# ------------------------------------------------------------
# exclude_unset=True
# ------------------------------------------------------------

print("\nexclude_unset=True:")

print(
    user.model_dump(
        exclude_unset=True
    )
)


# ------------------------------------------------------------
# exclude_defaults=True
# ------------------------------------------------------------

print("\nexclude_defaults=True:")

print(
    user.model_dump(
        exclude_defaults=True
    )
)


# ------------------------------------------------------------
# include={}
# ------------------------------------------------------------

print("\ninclude={name, email}:")

print(
    user.model_dump(
        include={
            "name",
            "email"
        }
    )
)


# ------------------------------------------------------------
# exclude={}
# ------------------------------------------------------------

print("\nexclude={email, phone}:")

print(
    user.model_dump(
        exclude={
            "email",
            "phone"
        }
    )
)


# ------------------------------------------------------------
# Nested include
# ------------------------------------------------------------

print("\nNested include:")

print(
    user.model_dump(
        include={
            "name": True,
            "address": {
                "city"
            }
        }
    )
)


# ------------------------------------------------------------
# Nested exclude
# ------------------------------------------------------------

print("\nNested exclude:")

print(
    user.model_dump(
        exclude={
            "address": {
                "country"
            }
        }
    )
)