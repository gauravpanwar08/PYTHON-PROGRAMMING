# ======================================================================================================
#                                PYDANTIC - COMPUTED FIELD
#
# computed_field() → Defines a computed field in the model based on values of other fields automatically.
# ========================================================================================================


from fastapi import FastAPI
from pydantic import BaseModel, computed_field


app = FastAPI()


# PYDANTIC MODEL

class Product(BaseModel):

    name: str
    price: float
    quantity: int


    # COMPUTED FIELD

    @computed_field
    @property
    def total_price(self) -> float:

        return self.price * self.quantity


# FASTAPI ENDPOINT

@app.post("/products")
def create_product(product: Product):

    return product