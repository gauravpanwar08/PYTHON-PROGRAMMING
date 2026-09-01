# Class Dependencies:
# Concept: class-based dependencies
# Using classes as dependencies in FastAPI.
#
# Commonly used for:
# - Pagination objects
# - Filters
# - Reusable request configurations
# -----------------------------------------------------------------

from fastapi import FastAPI, Depends

app = FastAPI()


class Pagination:
    def __init__(self, limit: int = 10):
        self.limit = limit


@app.get("/")
def home(data: Pagination = Depends()):
    return {
        "limit": data.limit
    }