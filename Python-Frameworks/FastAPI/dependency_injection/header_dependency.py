# Header Dependency:
# Concept: Dependency Injection with request headers.
#
# Commonly used for:
# - JWT authentication
# - API key validation
# - Authorization systems
# ---------------------------------------------------------------------------

from fastapi import FastAPI, Depends, Header

app = FastAPI()


def get_token(authorization: str = Header()):
    return authorization


@app.get("/profile")
def profile(token=Depends(get_token)):
    return {"token": token}
