# Concept: dependency inside dependency

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
    