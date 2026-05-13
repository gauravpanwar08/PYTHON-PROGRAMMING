from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id:int):
    return {
        "item_id": item_id,
        "message": f"Item with ID {item_id} has been retrieved successfully"
    }
    