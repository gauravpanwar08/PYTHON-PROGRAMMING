# Concept: app-wide dependency

from fastapi import FastAPI, Depends


def global_check():
    print("Global Dependency")


app = FastAPI(
    dependencies=[Depends(global_check)]
)

# This dependency will be executed for every request to any endpoint in the application.
@app.get("/")
def home():
    return {
        "message": "Home"
    }