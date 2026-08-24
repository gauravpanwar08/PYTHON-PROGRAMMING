# ============================================================
#       FASTAPI + PYTHON TYPING - TypedDict
#
# TypedDict     → Defines dictionary structure
# total=False   → Makes fields optional by default
# Required      → Makes a field required
# NotRequired   → Makes a field optional
#
# Important → TypedDict itself does NOT perform runtime
#             validation like Pydantic BaseModel.
# ============================================================

from typing import NotRequired, Required, TypedDict

from fastapi import FastAPI


app = FastAPI()


# ------------------------------------------------------------
# User TypedDict
# ------------------------------------------------------------

class User(TypedDict):

    name: Required[str]
    age: Required[int]
    email: Required[str]
    phone: NotRequired[str]


# ------------------------------------------------------------
# Create User
# ------------------------------------------------------------

@app.post("/users")
def create_user(user: User):

    return {
        "message": "User received",
        "user": user
    }


# ------------------------------------------------------------
# UserUpdate with total=False
# ------------------------------------------------------------

class UserUpdate(TypedDict, total=False):

    name: str
    age: int
    email: str
    phone: str


# ------------------------------------------------------------
# Update User
# ------------------------------------------------------------

@app.patch("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate
):

    return {
        "user_id": user_id,
        "updated_fields": user
    }


# ------------------------------------------------------------
# UserUpdate with Required
# ------------------------------------------------------------

class UserUpdateRequired(TypedDict, total=False):

    user_id: Required[int]
    name: str
    age: int
    email: str


# ------------------------------------------------------------
# Update User with Required ID
# ------------------------------------------------------------

@app.patch("/users/required/{user_id}")
def update_user_required(
    user_id: int,
    user: UserUpdateRequired
):

    return {
        "user_id": user_id,
        "update_data": user
    }


# ------------------------------------------------------------
# Product with Required + NotRequired
# ------------------------------------------------------------

class Product(TypedDict):

    id: Required[int]
    name: Required[str]
    description: NotRequired[str]
    price: NotRequired[float]


# ------------------------------------------------------------
# Create Product
# ------------------------------------------------------------

@app.post("/products")
def create_product(product: Product):

    return {
        "message": "Product received",
        "product": product
    }
