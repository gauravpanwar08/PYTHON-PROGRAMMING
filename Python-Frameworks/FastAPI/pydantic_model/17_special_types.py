# ============================================================
#             PYDANTIC - SPECIAL TYPES
#
# 1. EmailStr or email-validator
# 2. HttpUrl
# 3. UUID
# 4. datetime
# 5. date
# 6. Decimal
# ============================================================

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, HttpUrl, AnyUrl

app = FastAPI()

# USER MODEL


class User(BaseModel):

    # EmailStr
    # --------------------------------------------------------
    email: EmailStr

    # HttpUrl
    # --------------------------------------------------------
    website: HttpUrl
    
    # AnyUrl
    # --------------------------------------------------------
    url: AnyUrl

    # UUID
    # --------------------------------------------------------
    user_id: UUID

    # datetime
    # --------------------------------------------------------
    created_at: datetime

    # date
    # --------------------------------------------------------
    birth_date: date

    # Decimal
    # --------------------------------------------------------
    balance: Decimal


# CREATE USER

user = User(
    email="gaurav@example.com",
    website="https://example.com",
    url="ftp://files.example.com",
    user_id="550e8400-e29b-41d4-a716-446655440000",
    created_at="2026-08-23T10:30:00",
    birth_date="2004-05-15",
    balance="12500.50",
)


# CREATE USER


@app.post("/users")
def create_user(user: User):
    
    print("\n=================================\n")
    print("User:")
    print(user)

    print("\nEmail:")
    print(user.email)
    print(type(user.email))

    print("\nWebsite:")
    print(user.website)
    print(type(user.website))

    print("\nURL:")
    print(user.url)
    print(type(user.url))

    print("\nUser ID:")
    print(user.user_id)
    print(type(user.user_id))

    print("\nCreated At:")
    print(user.created_at)
    print(type(user.created_at))

    print("\nBirth Date:")
    print(user.birth_date)
    print(type(user.birth_date))

    print("\nBalance:")
    print(user.balance)
    print(type(user.balance))
    print("\n=================================\n")

    return {"message": "User created successfully",
            "user": user.model_dump()
            }
