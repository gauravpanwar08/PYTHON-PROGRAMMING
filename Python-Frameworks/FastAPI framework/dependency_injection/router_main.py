# Router with Dependencies:
# This file demonstrates how to include a router with dependencies in a FastAPI application.
# The router is defined in the `router_dependency` module, and it is included in the main application using `app.include_router()`.
# This allows you to organize your endpoints and their dependencies in a modular way.
# ----------------------------------------------------------------------------------------------------------------------------------

from fastapi import FastAPI

import router_dependency

app = FastAPI()

app.include_router(router_dependency.router)
