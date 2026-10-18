
# Define Pydantic schemas for creating and returning users

from pydantic import BaseModel, ConfigDict, Field, EmailStr


# User Create Schema
# Validates data received from the API client.

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int | None = Field(default=None, ge=1, le=120)


# User Response Schema
# Defines the fields returned by the API.

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    age: int | None
    is_active: bool
