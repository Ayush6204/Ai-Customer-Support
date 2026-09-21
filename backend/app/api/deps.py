from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.services.ownership_service import (
    validate_session_owner,
    validate_document_owner,
)
from typing import List

from app.core.security import decode_token
from app.db.database import get_db
from app.repositories.user_repository import get_user_by_id


bearer_scheme = HTTPBearer()

# this function is used as a dependency in routes to get the current user from the token
# This function checks who is logged in. It decodes the token, checks if it's valid, and retrieves the user from the database. It also checks if the user is active. If any of these checks fail, it raises an appropriate HTTP exception.
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = get_user_by_id(db, int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user

# these functions are used as dependencies in routes to ensure the user owns the resource they are trying to access
# This function checks:
# Does this chat session belong to the logged-in user?
def get_owned_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return validate_session_owner(
        db=db,
        session_id=session_id,
        current_user_id=current_user.id
    )

# this function is used as a dependency in routes to ensure the user owns the document they are trying to access
# This function checks:
# Does this document belong to the logged-in user?
def get_owned_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return validate_document_owner(
        db=db,
        document_id=document_id,
        current_user_id=current_user.id
    )


# this function is used as a dependency in routes to ensure the user has admin privileges
# This function checks:
# Is the current user an admin?
def require_admin(
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user

def require_role(allowed_roles: List[str]):
    """
    Role checker dependency.

    Example:
    current_user = Depends(require_role(["admin"]))
    """

    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker



def require_user(current_user=Depends(get_current_user)):
    """
    User-only dependency.

    Allows normal active users.
    Admin can also be allowed if you want admin to test user APIs.
    Here we allow both user and admin.
    """

    if current_user.role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User access required"
        )

    return current_user

