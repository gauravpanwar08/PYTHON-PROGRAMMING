# QUERY PARAMETERS - Used for: filtering, pagination, searching, optional values
# Example -/users?limit=5

from fastapi import FastAPI

app = FastAPI()

# Required parameters - have to be provided in the query string in the URL
@app.get('/products')
def get_products(category: str, price: float):
    return {
        'category': category,
        'price': price,
        "message": f"Products in category '{category}' with price less than {price}"
    }
    
# Optional parameters with default values
from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
def get_products(limit: int = 10, skip: int = 0):
    return {
        "limit": limit,
        "skip": skip,
        "message": "Query parameters working"
    }