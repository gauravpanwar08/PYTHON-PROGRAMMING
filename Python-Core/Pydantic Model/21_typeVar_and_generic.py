# ============================================================================================
#              PYTHON TYPING - TypeVar + Generic
#
# TypeVar  → Creates a reusable type variable that can represent different types
#            while preserving type information
#
# Generic  → Allows the same class/function/model structure to work with different data types
#            and type variable in a reusable way.
#
# Main Use → Reusable typed classes, functions and Pydantic models
# =============================================================================================


from typing import Generic, TypeVar

from pydantic import BaseModel


# ---------------------------------
# TYPE VARIABLE
# ---------------------------------

T = TypeVar("T")


# User model


class User(BaseModel):

    name: str
    age: int


# Product model


class Product(BaseModel):

    name: str
    price: float


# ----------------------------------------
# Generic response model
# ----------------------------------------


class Response(BaseModel, Generic[T]):

    success: bool
    message: str
    data: T


# User response

user_response = Response[User](
    success=True,
    message="User fetched successfully",
    data={"name": "Gaurav", "age": 22},
)

print("USER RESPONSE:")
print(user_response)

print("\nUser Data:")
print(user_response.data)


# Product response

product_response = Response[Product](
    success=True,
    message="Product fetched successfully",
    data={"name": "Laptop", "price": 75000},
)

print("\nPRODUCT RESPONSE:")
print(product_response)

print("\nProduct Data:")
print(product_response.data)


# Integer Response

int_response = Response[int](
    message="Integer fetched successfully", success=True, data=100
)

print("Integer Response:")
print(int_response)


# String Response

str_response = Response[str](
    message="String fetched successfully", success=True, data="Gaurav"
)

print("\nString Response:")
print(str_response)


# List Response

list_response = Response[list[str]](
    message="List of string fetched successfully",
    success=True,
    data=["Python", "FastAPI", "SQLAlchemy"],
)

print("\nList Response:")
print(list_response)
