"""Tests for authentication."""

from uuid import uuid4

import pytest

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import AuthService
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    get_user_id_from_token,
    verify_token,
)


class TestJWTTokens:
    """Tests for JWT token utilities."""

    def test_create_access_token(self):
        """Test access token creation."""
        user_id = uuid4()
        token = create_access_token(user_id)

        assert token is not None
        assert isinstance(token, str)

    def test_create_refresh_token(self):
        """Test refresh token creation."""
        user_id = uuid4()
        token = create_refresh_token(user_id)

        assert token is not None
        assert isinstance(token, str)

    def test_verify_access_token(self):
        """Test access token verification."""
        user_id = uuid4()
        token = create_access_token(user_id)

        payload = verify_token(token, token_type="access")

        assert payload is not None
        assert payload["sub"] == str(user_id)
        assert payload["type"] == "access"

    def test_verify_refresh_token(self):
        """Test refresh token verification."""
        user_id = uuid4()
        token = create_refresh_token(user_id)

        payload = verify_token(token, token_type="refresh")

        assert payload is not None
        assert payload["sub"] == str(user_id)
        assert payload["type"] == "refresh"

    def test_verify_token_wrong_type(self):
        """Test token verification with wrong type."""
        user_id = uuid4()
        access_token = create_access_token(user_id)

        # Try to verify access token as refresh token
        payload = verify_token(access_token, token_type="refresh")

        assert payload is None

    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        payload = verify_token("invalid-token")

        assert payload is None

    def test_get_user_id_from_token(self):
        """Test extracting user ID from token."""
        user_id = uuid4()
        token = create_access_token(user_id)

        extracted_id = get_user_id_from_token(token)

        assert extracted_id == user_id

    def test_get_user_id_from_invalid_token(self):
        """Test extracting user ID from invalid token."""
        extracted_id = get_user_id_from_token("invalid-token")

        assert extracted_id is None


class TestAuthService:
    """Tests for AuthService."""

    @pytest.mark.asyncio
    async def test_create_user(self, db_session):
        """Test user creation."""
        auth_service = AuthService(db_session)

        user_data = UserCreate(
            email="newuser@example.com",
            name="New User",
            google_id="google-new-123",
        )

        user = await auth_service.create_user(user_data)

        assert user is not None
        assert user.email == "newuser@example.com"
        assert user.name == "New User"
        assert user.google_id == "google-new-123"
        assert user.is_active is True

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, db_session, test_user):
        """Test getting user by email."""
        auth_service = AuthService(db_session)

        user = await auth_service.get_user_by_email("test@example.com")

        assert user is not None
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_user_by_google_id(self, db_session, test_user):
        """Test getting user by Google ID."""
        auth_service = AuthService(db_session)

        user = await auth_service.get_user_by_google_id("google-123")

        assert user is not None
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_or_create_user_existing(self, db_session, test_user):
        """Test get_or_create with existing user."""
        auth_service = AuthService(db_session)

        user_data = UserCreate(
            email="test@example.com",
            name="Test User Updated",
            google_id="google-123",
        )

        user, created = await auth_service.get_or_create_user(user_data)

        assert created is False
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_or_create_user_new(self, db_session):
        """Test get_or_create with new user."""
        auth_service = AuthService(db_session)

        user_data = UserCreate(
            email="brand-new@example.com",
            name="Brand New User",
            google_id="google-brand-new",
        )

        user, created = await auth_service.get_or_create_user(user_data)

        assert created is True
        assert user.email == "brand-new@example.com"

    @pytest.mark.asyncio
    async def test_create_tokens(self, db_session, test_user):
        """Test token creation."""
        auth_service = AuthService(db_session)

        tokens = auth_service.create_tokens(test_user.id)

        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_get_current_user(self, db_session, test_user):
        """Test getting current user from token."""
        auth_service = AuthService(db_session)
        access_token = create_access_token(test_user.id)

        user = await auth_service.get_current_user(access_token)

        assert user is not None
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self, db_session):
        """Test getting current user with invalid token."""
        auth_service = AuthService(db_session)

        user = await auth_service.get_current_user("invalid-token")

        assert user is None

    @pytest.mark.asyncio
    async def test_refresh_access_token(self, db_session, test_user):
        """Test refreshing access token."""
        auth_service = AuthService(db_session)
        refresh_token = create_refresh_token(test_user.id)

        tokens = await auth_service.refresh_access_token(refresh_token)

        assert tokens is not None
        assert "access_token" in tokens
        assert "refresh_token" in tokens
