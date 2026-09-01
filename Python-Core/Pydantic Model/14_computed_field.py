# ======================================================================================================
#                                PYDANTIC - COMPUTED FIELD
#
# computed_field() → Defines a computed field in the model based on values of other fields automatically.
# ========================================================================================================


from pydantic import BaseModel, computed_field


class Product(BaseModel):

    name: str
    price: float
    quantity: int


    # COMPUTED FIELD

    @computed_field
    @property
    def total_price(self) -> float:

        return self.price * self.quantity


# CREATE MODEL INSTANCE

product = Product(
    name="Laptop",
    price=50000,
    quantity=2
)


# ACCESS COMPUTED FIELD

print("Product:")
print(product)

print("\nTotal Price:")
print(product.total_price)


# model_dump()

print("\nModel Dump:")
print(product.model_dump())