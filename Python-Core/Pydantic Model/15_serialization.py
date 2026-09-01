# ============================================================
#       PYDANTIC - JSON SERIALIZATION & VALIDATION
#
# model_dump()
#     Pydantic Model → Dictionary
#
# model_dump_json()
#     Pydantic Model → JSON String
#
# model_validate()
#     Dictionary → Pydantic Model
#
# model_validate_json()
#     JSON String → Pydantic Model
# ============================================================

"""         PYDANTIC MODEL
                   │
      ┌────────────┴────────────┐
      │                         │
model_dump()            model_dump_json()
      │                         │
      ↓                         ↓
 Dictionary                JSON String
      │                         │
      │                         │
model_validate()      model_validate_json()
      │                         │
      └────────────┬────────────┘
                   ↓
            PYDANTIC MODEL
"""


from pydantic import BaseModel

# USER MODEL

class User(BaseModel):

    name: str
    age: int
    email: str

# CREATE PYDANTIC MODEL

user = User(
    name="Gaurav",
    age=22,
    email="gaurav@example.com"
)


# ---------------------------------------------------------------------
# 1. model_dump() ->> Convert Pydantic Model into Dictionary
# ---------------------------------------------------------------------

user_dict = user.model_dump()

print("1. model_dump():")
print(user_dict)

print("\nType:")
print(type(user_dict))


# ---------------------------------------------------------------------
# 2. model_dump_json() ->> Convert Pydantic Model into JSON String
# ---------------------------------------------------------------------

user_json = user.model_dump_json()

print("\n2. model_dump_json():")
print(user_json)

print("\nType:")
print(type(user_json))


# ---------------------------------------------------------------------
# 3. model_validate() ->> Convert Dictionary into Pydantic Model
# ---------------------------------------------------------------------

new_user_dict = {
    "name": "Rahul",
    "age": 24,
    "email": "rahul@example.com"
}

new_user = User.model_validate(new_user_dict)

print("\n3. model_validate():")
print(new_user)

print("\nType:")
print(type(new_user))


# ---------------------------------------------------------------------
# 4. model_validate_json() ->> Convert JSON String into Pydantic Model
# ---------------------------------------------------------------------

user_json_data = """
{
    "name": "Aman",
    "age": 25,
    "email": "aman@example.com"
}
"""

user_from_json = User.model_validate_json(
    user_json_data
)

print("\n4. model_validate_json():")
print(user_from_json)

print("\nType:")
print(type(user_from_json))

