# ============================================================
#         model_dump() + model_validate() Together
# ============================================================


from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    email: str


# ------------------------------------------------------------
# Create Pydantic Model
# ------------------------------------------------------------

user1 = User(
    name="Gaurav",
    age=22,
    email="gaurav@example.com"
)

print("Original Model:")
print(user1)


# ------------------------------------------------------------
# Pydantic Model → Dictionary
# ------------------------------------------------------------

user_data = user1.model_dump()

print("\nDictionary:")
print(user_data)


# ------------------------------------------------------------
# Dictionary → Pydantic Model
# ------------------------------------------------------------

user2 = User.model_validate(user_data)

print("\nNew Pydantic Model:")
print(user2)
