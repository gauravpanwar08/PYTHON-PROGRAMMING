# ============================================================
#        PYDANTIC - JSON SERIALIZATION and DESERIALIZATION
#
# Methods covered:
#
# 1. model_dump()
#       Pydantic Model → Dictionary
#
# 2. model_dump_json()
#       Pydantic Model → JSON String
#
# 3. model_validate()
#       Dictionary → Pydantic Model
#
# 4. model_validate_json()
#       JSON String → Pydantic Model
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


from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# USER MODEL

class User(BaseModel):
    name: str
    age: int
    email: str


# ---------------------------------------------------------------------
# 1. model_dump() ->> Convert Pydantic Model into Dictionary
# ---------------------------------------------------------------------

@app.post("/users/dump")
def model_dump(user: User):

    # Convert Pydantic Model into Dictionary

    user_data = user.model_dump()

    print("Pydantic Object:")
    print(user)

    print("\nDictionary:")
    print(user_data)

    print("\nType:")
    print(type(user_data))

    return {
        "message": "model_dump() example",
        "data": user_data
    }


# ---------------------------------------------------------------------
# 2. model_dump_json() ->> Convert Pydantic Model into JSON String
# ---------------------------------------------------------------------

@app.post("/users/dump-json")
def model_dump_json(user: User):

    # Convert Pydantic Model into JSON String

    user_json = user.model_dump_json()

    print("Pydantic Object:")
    print(user)

    print("\nJSON String:")
    print(user_json)

    print("\nType:")
    print(type(user_json))

    return {
        "message": "model_dump_json() example",
        "data": user_json
    }


# ---------------------------------------------------------------------
# 3. model_validate() ->> Convert Dictionary into Pydantic Model
# ---------------------------------------------------------------------

@app.post("/users/validate")
def model_validate(user_data: dict):

    # Validate dictionary and create Pydantic Model

    user = User.model_validate(user_data)

    print("Dictionary:")
    print(user_data)

    print("\nPydantic Object:")
    print(user)

    print("\nType:")
    print(type(user))

    return {
        "message": "model_validate() example",
        "data": user.model_dump()
    }


# ---------------------------------------------------------------------
# 4. model_validate_json() ->> Convert JSON String into Pydantic Model
# ---------------------------------------------------------------------

@app.post("/users/validate-json")
def model_validate_json(json_data: str):

    # Validate JSON string and create Pydantic Model

    user = User.model_validate_json(json_data)

    print("JSON String:")
    print(json_data)

    print("\nPydantic Object:")
    print(user)

    print("\nType:")
    print(type(user))

    return {
        "message": "model_validate_json() example",
        "data": user
    }

