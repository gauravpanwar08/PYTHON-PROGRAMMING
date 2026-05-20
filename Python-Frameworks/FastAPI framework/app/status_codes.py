"""
HTTP status code is a three-digit response sent by a server to a browser (or client) indicating the outcome of a request.
These status code helps the client understand whether the request was successful, if there was an error, or if further action is needed.
"""

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str

# GET request
@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
def read_item(item_id: int):
    return {"item_id": item_id}

# POST request
@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return {"name": item.name}

# PUT request
@app.put("/items/{item_id}", status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "name": item.name}

# DELETE request
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return {
        "message": f"Item with id {item_id} has been deleted"
    }
