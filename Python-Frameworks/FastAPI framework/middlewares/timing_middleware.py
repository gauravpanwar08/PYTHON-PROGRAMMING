# Timing Middleware: Measures request processing time.


import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def timing_middleware(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    end_time = time.time()

    process_time = end_time - start_time

    response.headers["X-Process-Time"] = str(process_time)

    print(f"Process Time: {process_time}")

    return response


@app.get("/")
def home():

    return {
        "message": "Timing Middleware Example"
    }