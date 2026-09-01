# RESPONSE MODEL:
# Used to control and validate outgoing API responses.
# A response model is a structured data framework that defines, validates, and formats the information
# then sent back to a user or client after receiving a request.
#
# Commonly used for:
# - Hiding passwords/tokens
# - Standardizing responses
# ------------------------------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
    
@app.get("/users/", response_model=UserResponse)
async def read_user():
    return {
        'id': 1,
        "name": "Gaurav",
        "age": 23,
        "email": "gaurav@example.com",
        "pa": "s"
    }