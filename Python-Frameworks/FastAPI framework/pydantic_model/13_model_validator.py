# ============================================================
#             PYDANTIC - MODEL VALIDATOR
#
# model_validator() → Validates the entire model OR multiple
# fields at once whose validation/relationship depends on each other
#
# mode="before" → Before Validation/type conversion
# mode="after"  → After Validation/type conversion
#                 and it is the default mode
# ============================================================


from fastapi import FastAPI
from pydantic import BaseModel, model_validator


app = FastAPI()


# PYDANTIC MODEL

class User(BaseModel):

    username: str
    password: str
    confirm_password: str


    # MODEL VALIDATOR

    @model_validator(mode="after")
    def check_passwords(self):

        if self.password != self.confirm_password:

            raise ValueError(
                "Password and confirm password must match"
            )

        return self


# FASTAPI ENDPOINT

@app.post("/users")
def create_user(user: User):

    return {
        "message": "User created successfully",
        "user": user
    }
