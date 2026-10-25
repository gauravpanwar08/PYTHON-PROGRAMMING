
# Test JWT creation, decoding, and expiration verification.

from datetime import timedelta

from jwt.exceptions import InvalidTokenError

from auth.token import (
    create_access_token,
    decode_access_token,
)


token = create_access_token(
    data={"sub": "123"},
)

print("JWT:", token)

payload = decode_access_token(token)

print("User ID:", payload["sub"])
print("Expiration:", payload["exp"])


# Verify that an expired token is rejected.
expired_token = create_access_token(
    data={"sub": "123"},
    expires_delta=timedelta(seconds=-1),
)

try:
    decode_access_token(expired_token)
except InvalidTokenError:
    print("Expired token rejected successfully.")
