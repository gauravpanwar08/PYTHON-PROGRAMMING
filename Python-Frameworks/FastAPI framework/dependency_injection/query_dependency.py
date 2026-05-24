# Concept: reusable query params

from fastapi import FastAPI, Depends

app = FastAPI()


def pagination(limit: int = 10, skip: int = 0):
    return {
        "limit": limit,
        "skip": skip
        }


@app.get("/products")
def get_products(data=Depends(pagination)):
    return data
