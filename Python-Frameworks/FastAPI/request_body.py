# REQUEST BODY:
# used to control and validate incoming API requests.
# Used to receive data from the client in JSON format.
# Mostly used in POST, PUT, and PATCH requests.
# A request body is the data sent by a client (like a browser or a mobile app) to a server as part of an API request. 
# It typically contains information that the server needs to process the request, such as user input, form data, or JSON payloads.
# ------------------------------------------------------------------------------

# Option 1: Using FastAPI
from fastapi import FastAPI

app = FastAPI()

@app.post("/products")
def create_product(product: dict):
    return {
        "received_data": product,
        "message":"Product created successfully"
    }


# Option 2: Using Raw Request Object (For completely dynamic JSON)
# If you do not want to pre-define any keys and want to accept absolutely any JSON layout the client sends, you can parse the raw request body manually.

from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/dynamic-data")
async def handle_raw_json(request: Request):
    """Reads the entire raw JSON body as a standard Python dictionary."""
    
    # Extracting the raw JSON payload
    data = await request.json()
    
    return {
        "message": "Raw JSON parsed successfully",
        "your_data": data
    }
