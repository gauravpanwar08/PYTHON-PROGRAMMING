# Logging Middleware: Logs request information.


from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def logging_middleware(request: Request, call_next):

    print(f"Method: {request.method}")

    print(f"URL: {request.url}")

    response = await call_next(request)

    return response


@app.get("/")
def home():

    return {
        "message": "Logging Middleware Example"
    }