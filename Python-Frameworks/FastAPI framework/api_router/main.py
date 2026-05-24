# Main Application Entry Point & Router Registry
# Main FastAPI application that includes multiple routers.


from fastapi import FastAPI

# Importing isolated router configurations from the project module layers
from api_router.routers import users
from api_router.routers import products

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)

