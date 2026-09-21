from datetime import datetime
from sqlalchemy.orm import Session

from app.models.token_blacklist import TokenBlacklist


def blacklist_token(
    db: Session,
    user_id: int,
    jti: str,
    token_type: str,
    expires_at: datetime
):
    blacklisted_token = TokenBlacklist(
        user_id=user_id,
        jti=jti,
        token_type=token_type,
        expires_at=expires_at
    )

    db.add(blacklisted_token)
    db.commit()
    db.refresh(blacklisted_token)

    return blacklisted_token


def is_token_blacklisted(db: Session, jti: str) -> bool:
    token = db.query(TokenBlacklist).filter(
        TokenBlacklist.jti == jti
    ).first()

    return token is not None