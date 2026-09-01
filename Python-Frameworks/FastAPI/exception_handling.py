# Exception Handling
# Used to handle errors and return proper API responses.
#
# Common Uses:
# - Resource not found
# - Unauthorized access
# - Invalid operations
# - Custom error handling
# ------------------------------------------------------------------------------------


from fastapi import FastAPI, HTTPException, status

from fastapi import Request                    # For Custom Exception Handler
from fastapi.responses import JSONResponse     # For Custom Exception Handler


app = FastAPI()


products = {1: "Laptop",
            2: "Phone"}


@app.get("/products/{product_id}")
def get_product(product_id: int):

    product = products.get(product_id)

    if not product:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {"product_id": product_id,
            "product_name": product
    }


# Unauthorized Access Example

@app.get("/admin")
def admin(password: str):

    if password != "admin123":

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return {
        "message": "Welcome Admin"
    }
    

# Custom Exception Handler

@app.get("/custom-error")
def custom_error():

    raise ValueError("Custom error")

@app.exception_handler(ValueError)
def value_error_handler(request: Request, exc: ValueError):

    return JSONResponse(
        status_code=400,
        content={
            "message": str(exc)
        }
    )
    
