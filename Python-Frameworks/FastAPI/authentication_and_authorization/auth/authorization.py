# Provides reusable role-based authorization for protected endpoints.

from typing import Annotated

from fastapi import Depends, HTTPException, status

from auth.dependencies import CurrentUser


def require_role(required_role: str):
    """Allow access only to users with the required role."""

    def role_checker(
        current_user: CurrentUser,
    ) -> dict:
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker


AdminUser = Annotated[dict, Depends(require_role("admin"))]
