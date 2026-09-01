# ============================================================
#               PYDANTIC - model_validate()
#
# model_validate() is used to validate data and create a Pydantic model instance from that data.
# Dictionary / external data --> model_validate() --> Pydantic Model --> FastAPI Response
# =================================================================

from pydantic import BaseModel
from fastapi import FastAPI


app = FastAPI()


class User(BaseModel):
    name: str
    age: int
    email: str


# Dictionary/External/Database Data 

user_data = {
    "name": "Gaurav",
    "age": 22,
    "email": "gaurav@example.com"
}


# Validate Dictionary/External Data and Create Pydantic Model
# Dictionary → Pydantic Model

@app.get("/users")
def get_user():

    user = User.model_validate(user_data)

    print("Pydantic Object:")
    print(user)

    return user
