# ============================================================
# PYDANTIC -> NORMAL Field() vs Annotated + Field()
# Both approaches perform the same type of validation.
#
# Normal Field Format-
#     name: str = Field(min_length=3)
#
# Annotated Format-
#     name: Annotated[str, Field(min_length=3)]
# ============================================================


from typing import Annotated
from pydantic import BaseModel, Field


# NORMAL Field()
# -------------------------------------------

class UserNormal(BaseModel):

    # Type + Field directly on the field
    name: str = Field(
        min_length=3,
        max_length=50
    )

    age: int = Field(
        ge=18,
        le=100
    )

    username: str = Field(
        min_length=3,
        max_length=20
    )


# Annotated + Field()
# ----------------------------------------------------

class UserAnnotated(BaseModel):

    # Type and validation metadata are separated
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50
        )
    ]

    age: Annotated[
        int,
        Field(
            ge=18,
            le=100
        )
    ]

    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=20
        )
    ]


# CREATE USER USING NORMAL Field()

user_normal = UserNormal(
    name="Gaurav",
    age=22,
    username="gaurav08"
)

print("NORMAL Field():")
print(user_normal)


# CREATE USER USING Annotated + Field()

user_annotated = UserAnnotated(
    name="Gaurav",
    age=22,
    username="gaurav08"
)

print("\nANNOTATED + Field():")
print(user_annotated)


# BOTH PRODUCE SAME KIND OF DATA

print("\nNormal Field Dictionary:")
print(user_normal.model_dump())

print("\nAnnotated Dictionary:")
print(user_annotated.model_dump())