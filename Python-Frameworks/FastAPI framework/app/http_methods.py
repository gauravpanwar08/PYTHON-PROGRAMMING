# HTTP methods communicate the specific action a client wants to perform on a server resource.
"""
This is foundation of CRUD APIs and mostly used methods:
GET     → fetch/read
POST    → create
PUT     → update
DELETE  → remove
PATCH   → partial update
"""

from fastapi import FastAPI

app = FastAPI()

# GET Request - Used to fetch/read/retrieve data from the server.
@app.get("/products")
def get_products():
    return {"message": "Get all products"}


# POST Request - Used to create new resources.
@app.post("/products")
def create_product():
    return {"message": "Product created"}


# PUT Request - Used to update a resource by replacing it entirely.
@app.put("/products/{product_id}")
def update_product(product_id: int):
    return {
        "message": f"Product {product_id} updated"
    }

# PATCH Request - Used for partial updates to an existing resource.
@app.patch("/products/{product_id}")
def partial_update_product(product_id: int):
    return {
        "message": f"Product {product_id} partially updated"
    }

# DELETE Request - Used to remove a resource from the server.
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return {
        "message": f"Product {product_id} deleted"
    }


# Advanced but Rarely Used Methods - FastAPI also supports other standard HTTP methods for specialized communication.
"""
OPTIONS	→ Allowed methods info
HEAD	→ Headers only
TRACE	→ Diagnostic/debug
CONNECT	→ Tunnel connection
"""

# @app.options(): Returns the communication options available for the target resource.
# @app.head(): Retrieves the response headers identical to a GET request, but without the response body.
# @app.trace(): Performs a message loop-back test along the path to the target resource.