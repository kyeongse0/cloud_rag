"""Authentication API endpoints."""

from typing import Annotated

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import AuthService

router = APIRouter()
settings = get_settings()

# OAuth setup
oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Dependency for auth service."""
    return AuthService(db)


@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login flow."""
    redirect_uri = settings.google_redirect_uri
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Handle Google OAuth callback."""
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"OAuth authentication failed: {str(e)}",
        )

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get user info from Google",
        )

    # Create or get user
    user_data = UserCreate(
        email=user_info["email"],
        name=user_info.get("name", user_info["email"]),
        profile_image=user_info.get("picture"),
        google_id=user_info["sub"],
    )
    user, _ = await auth_service.get_or_create_user(user_data)

    # Create JWT tokens
    tokens = auth_service.create_tokens(user.id)

    # Redirect to frontend with tokens in httpOnly cookies
    response = RedirectResponse(url="http://localhost:5173/dashboard")
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
    )
    return response


@router.post("/refresh")
async def refresh_token(
    refresh_token: Annotated[str | None, Cookie()] = None,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Refresh access token using refresh token."""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not provided",
        )

    tokens = await auth_service.refresh_access_token(refresh_token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    response = RedirectResponse(url="/", status_code=status.HTTP_200_OK)
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return {"message": "Token refreshed successfully"}


@router.post("/logout")
async def logout():
    """Logout user by clearing cookies."""
    response = RedirectResponse(url="http://localhost:5173/")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    access_token: Annotated[str | None, Cookie()] = None,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Get current authenticated user."""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    user = await auth_service.get_current_user(access_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user
