# Concept: Basic Depends() and return value injection

from fastapi import FastAPI, Depends

app = FastAPI()


def get_message():
    return "Hello, Gaurav! Dependency Injection executed successfully."


@app.get("/")
def home(message: str = Depends(get_message)):
    return {"message": message}
