from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    LogoutRequest,
    AuthMessageResponse,
)
from app.schemas.user_schema import UserResponse
from app.services.auth_service import (
    register_user,
    login_user,
    refresh_user_token,
    logout_user,
)
from app.api.deps import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    
    user = register_user(
        db=db,
        name=request.name,
        email=request.email,
        password=request.password
    )
    return user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    tokens = login_user(
        db=db,
        email=request.email,
        password=request.password
    )

    return tokens


@router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    tokens = refresh_user_token(
        db=db,
        refresh_token=request.refresh_token
    )

    return tokens


@router.post(
    "/logout",
    response_model=AuthMessageResponse
)
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db)
):
    result = logout_user(
        db=db,
        refresh_token=request.refresh_token
    )

    return result


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user