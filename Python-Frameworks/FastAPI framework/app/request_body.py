"""
A request body is the data sent by a client (like a browser or a mobile app) to a server as part of an API request. 
It typically contains information that the server needs to process the request, such as user input, form data, or JSON payloads.
"""

from fastapi import FastAPI

app = FastAPI()

@app.post("/products")
def create_product(product: dict):
    return {
        "received_data": product,
        "message":"Product created successfully"
    }
