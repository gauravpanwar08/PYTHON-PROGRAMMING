# ====================================================================
#                 PYTHON TYPING - TypeAlias
#
# TypeAlias → Gives a meaningful name to an existing type.
# Main Use → Makes complex/repeated type annotations reusable/readable
# =====================================================================


from typing import TypeAlias

# ------------------------------------------------------------
# Simple Type Aliases
# ------------------------------------------------------------

UserID: TypeAlias = int

UserName: TypeAlias = str


user_id: UserID = 101

user_name: UserName = "Gaurav"


print("User ID:")
print(user_id)

print("\nUser Name:")
print(user_name)


# ------------------------------------------------------------
# List Type Alias
# ------------------------------------------------------------

Scores: TypeAlias = list[int]


scores: Scores = [90, 85, 95]

print("\nScores:")
print(scores)


# ------------------------------------------------------------
# Dictionary Type Alias
# ------------------------------------------------------------

UserData: TypeAlias = dict[str, str | int | bool]


user: UserData = {"name": "Gaurav", "age": 22, "is_active": True}

print("\nUser Data:")
print(user)


# ------------------------------------------------------------
# Nested Type Alias
# ------------------------------------------------------------

Users: TypeAlias = list[UserData]


users: Users = [
    {"name": "Gaurav", "age": 22, "is_active": True},
    {"name": "Rahul", "age": 23, "is_active": False},
]

print("\nUsers:")
print(users)


# ------------------------------------------------------------
# Function using TypeAlias
# ------------------------------------------------------------


def get_user(user: UserData) -> UserData:

    return user


result = get_user(user)

print("\nFunction Result:")
print(result)
