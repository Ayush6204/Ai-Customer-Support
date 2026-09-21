from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.repositories.user_repository import (
    get_user_by_email,
    create_user,
    get_user_by_id,
)
from app.repositories.token_repository import (
    blacklist_token,
    is_token_blacklisted,
)


def register_user(db: Session, name: str, email: str, password: str):
    existing_user = get_user_by_email(db, email)
    print(existing_user)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(password)
    print("hashed_password", hashed_password)
    
    user = create_user(
        db=db,
        name=name,
        email=email,
        hashed_password=hashed_password,
        role="user"
    )
    return user


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_user_token(db: Session, refresh_token: str):
    payload = decode_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    jti = payload.get("jti")
    user_id = payload.get("sub")
    exp = payload.get("exp")

    if not jti or not user_id or not exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    if is_token_blacklisted(db, jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token already used or logged out"
        )

    user = get_user_by_id(db, int(user_id))

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    expires_at = datetime.fromtimestamp(exp, timezone.utc)

    blacklist_token(
        db=db,
        user_id=user.id,
        jti=jti,
        token_type="refresh",
        expires_at=expires_at
    )

    new_access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


def logout_user(db: Session, refresh_token: str):
    payload = decode_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    jti = payload.get("jti")
    user_id = payload.get("sub")
    exp = payload.get("exp")

    if not jti or not user_id or not exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    if is_token_blacklisted(db, jti):
        return {
            "message": "User already logged out"
        }

    expires_at = datetime.fromtimestamp(exp, timezone.utc)

    blacklist_token(
        db=db,
        user_id=int(user_id),
        jti=jti,
        token_type="refresh",
        expires_at=expires_at
    )

    return {
        "message": "Logout successful"
    }