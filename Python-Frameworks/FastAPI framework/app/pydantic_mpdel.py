from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name : str
    age : int
    email : str
    
@app.post("/users")
def create_user(user: User):
    return {
        "received_user_data": user,
        "message": "User created successfully"
    }
    