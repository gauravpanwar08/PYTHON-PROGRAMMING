# Concept: class-based dependencies

from fastapi import FastAPI, Depends

app = FastAPI()


class Pagination:
    def __init__(self, limit: int = 10):
        self.limit = limit


@app.get("/")
def home(data: Pagination = Depends()):
    return {
        "limit": data.limit
    }