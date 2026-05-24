# INTRODUCTION TO FASTAPI:
# FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
# ----------------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Concepts",
    description="A collection of FastAPI concepts and examples"
)

@app.get("/")
def home():
    return {"message": "FastAPI is working"}