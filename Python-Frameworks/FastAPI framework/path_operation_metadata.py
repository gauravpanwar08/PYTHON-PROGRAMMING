# PATH OPERATION METADATA:
# Used to add extra information to API endpoints.
#
# Benefits:
# - Better Swagger documentation
# - Professional API structure
# - Clear endpoint descriptions
# - Organized API docs
# -----------------------------------------------------------------------------------

from fastapi import FastAPI, status

# Initialize the main FastAPI application instance
app = FastAPI(
    title="E-Commerce API",
    description="A complete API for managing product catalogs using route metadata.",
    version="1.0.0",
)


@app.get(
    "/products",
    tags=["Products"],
    summary="Get all products",
    description="""
## Product Endpoint

This endpoint returns all products.

### Features
- Fast response
- Pagination support
- Filtering support
""",
    response_description="List of products returned successfully",
    status_code=status.HTTP_200_OK,
)
def get_products():

    return {
        "products": [
            {"id": 1, "name": "Laptop", "price": 899.99},
            {"id": 2, "name": "Phone", "price": 499.99},
        ]
    }


@app.post(
    "/products",
    tags=["Products"],
    summary="Create a new product",
    description="This endpoint creates a new product in the database.",
    response_description="Product created successfully",
    status_code=status.HTTP_201_CREATED,
)
def create_product():

    return {
        "message": "Product created successfully",
        "product": {"id": 3, "name": "Tablet", "price": 299.99},
    }


@app.get("/old-route", deprecated=True)
def get_products():
    return {"message": "This route is deprecated. Please use /products instead."}
