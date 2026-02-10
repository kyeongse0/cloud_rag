"""Authentication service."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    get_user_id_from_token,
)

settings = get_settings()


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_google_id(self, google_id: str) -> User | None:
        """Get user by Google ID."""
        result = await self.db.execute(select(User).where(User.google_id == google_id))
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        is_admin = user_data.email in settings.admin_email_list

        user = User(
            email=user_data.email,
            name=user_data.name,
            profile_image=user_data.profile_image,
            google_id=user_data.google_id,
            is_admin=is_admin,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_or_create_user(self, user_data: UserCreate) -> tuple[User, bool]:
        """Get existing user or create new one.

        Returns (user, created) where created is True if user was created.
        """
        user = await self.get_user_by_google_id(user_data.google_id)
        if user:
            # Update profile info if changed
            if user.name != user_data.name or user.profile_image != user_data.profile_image:
                user.name = user_data.name
                user.profile_image = user_data.profile_image
                await self.db.flush()
            return user, False

        user = await self.create_user(user_data)
        return user, True

    def create_tokens(self, user_id: UUID) -> dict[str, str]:
        """Create access and refresh tokens for a user."""
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_access_token(self, refresh_token: str) -> dict[str, str] | None:
        """Refresh access token using refresh token.

        Returns new tokens if valid, None if invalid.
        """
        user_id = get_user_id_from_token(refresh_token, token_type="refresh")
        if user_id is None:
            return None

        user = await self.get_user_by_id(user_id)
        if user is None or not user.is_active:
            return None

        return self.create_tokens(user.id)

    async def get_current_user(self, access_token: str) -> User | None:
        """Get current user from access token."""
        user_id = get_user_id_from_token(access_token, token_type="access")
        if user_id is None:
            return None

        user = await self.get_user_by_id(user_id)
        if user is None or not user.is_active:
            return None

        return user
