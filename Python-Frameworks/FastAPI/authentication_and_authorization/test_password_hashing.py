
# Test password hashing and verification.

from auth.password_hashing import (
    hash_password,
    verify_password,
)

password = "MyStrongPassword123!"

hashed_password = hash_password(password)

print("Hashed password:", hashed_password)
print("Correct password:", verify_password(password, hashed_password))
print("Wrong password:", verify_password("wrong-password", hashed_password))
