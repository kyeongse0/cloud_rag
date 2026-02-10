"""User Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    name: str
    profile_image: str | None = None


class UserCreate(UserBase):
    """Schema for creating a user."""

    google_id: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    name: str | None = None
    profile_image: str | None = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: UUID
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserInDB(UserResponse):
    """Schema for user in database."""

    google_id: str


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""

    sub: str
    exp: datetime
    type: str
