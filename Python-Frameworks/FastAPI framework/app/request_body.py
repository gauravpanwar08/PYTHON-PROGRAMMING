from fastapi import FastAPI

app = FastAPI()

@app.post("/products")
def create_product(product: dict):
    return {
        "received_data": product,
        "message":"Product created successfully"
    }
