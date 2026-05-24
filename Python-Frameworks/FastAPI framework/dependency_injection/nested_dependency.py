# Nested Dependencies:
# Concept: dependency inside dependency
# A dependency can depend on another dependency.
#
# Commonly used in:
# - Authentication chains
# - User verification
# - Permission systems
# ---------------------------------------------------------------------------

from fastapi import FastAPI, Depends

app = FastAPI()


def verify_token():
    return "valid token"


def get_current_user(token = Depends(verify_token)):
    return "Gaurav"


@app.get("/")
def home(user = Depends(get_current_user)):
    return {
        "user": user
    }
    