# Router Dependency: router-level dependency

from fastapi import Depends, APIRouter


def verify_user():
    print("Verifying user...")
    return "User verified"


router = APIRouter(
    prefix="/users",
    dependencies=[Depends(verify_user)]
)

# also can be written as: router.dependencies.append(Depends(verify_user))

@router.get("/")
def users():
    return {
        "message": "Welcome to the users router!"
    }