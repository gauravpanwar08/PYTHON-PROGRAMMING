# CORS Middleware:
# CORS = Cross-Origin Resource Sharing, where Origin = Protocol + Domain + Port
# Allows frontend applications to access backend APIs.
#--------------------------------------------------------------------------------


from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500"
]


app.add_middleware(
    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


@app.get("/")
def home():

    return {
        "message": "CORS Middleware Example"
    }