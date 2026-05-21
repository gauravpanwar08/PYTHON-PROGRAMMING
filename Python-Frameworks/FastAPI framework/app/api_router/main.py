from fastapi import FastAPI

from app.api_router.routers import users
from app.api_router.routers import products

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)

