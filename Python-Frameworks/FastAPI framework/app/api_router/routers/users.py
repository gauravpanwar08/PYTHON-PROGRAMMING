from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/users")
def get_users():
    return {
        "message": "All users"
    }


@router.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }
