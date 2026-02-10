"""Security utilities for JWT token management."""

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()


def create_access_token(user_id: UUID, expires_delta: timedelta | None = None) -> str:
    """Create a new access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(user_id: UUID, expires_delta: timedelta | None = None) -> str:
    """Create a new refresh token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token: str, token_type: str = "access") -> dict[str, Any] | None:
    """Verify and decode a JWT token.

    Returns the payload if valid, None if invalid.
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str, token_type: str = "access") -> UUID | None:
    """Extract user ID from a token.

    Returns UUID if valid, None if invalid.
    """
    payload = verify_token(token, token_type)
    if payload is None:
        return None

    user_id_str = payload.get("sub")
    if user_id_str is None:
        return None

    try:
        return UUID(user_id_str)
    except ValueError:
        return None
