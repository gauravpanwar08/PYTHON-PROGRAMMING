# Yield Dependencies:
# Used for setup and cleanup operations during request lifecycle.
#
# Commonly used for:
# - Database sessions
# - Resource management
# - Connection cleanup
# ---------------------------------------------------------------------------

from fastapi import FastAPI, Depends

app = FastAPI()


def lifecycle_dependency():
    print("Before yield: setup resources")   # before routes execution
    yield "Resources is ready"               # Observe terminal output
    print("After yield: cleanup resources")  # after routes execution


@app.get("/")
def home(data=Depends(lifecycle_dependency)):
    return {"message": data}
