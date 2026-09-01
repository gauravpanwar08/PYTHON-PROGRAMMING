# Middleware:
# Middleware runs before and after every request.
#
# Common Uses:
# - Logging
# - Authentication
# - Request timing
# - Security checks
# - Monitoring
# ------------------------------------------------------------


from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def basic_middleware(request: Request, call_next):
    print("Before request")
    response = await call_next(request)
    print("After request")
    return response


@app.get("/")
def home():
    return {"message": "Basic Middleware Example"}
