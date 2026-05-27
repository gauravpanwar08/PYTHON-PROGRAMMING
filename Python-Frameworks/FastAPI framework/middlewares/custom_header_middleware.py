# Custom Header Middleware: Adds custom headers to every response.


from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def custom_header_middleware(request: Request, call_next):

    response = await call_next(request)

    response.headers["X-App-Name"] = "FastAPI Learning"

    response.headers["X-Developer"] = "Gaurav"

    return response


@app.get("/")
def home():

    return {
        "message": "Custom Header Middleware Example"
    }