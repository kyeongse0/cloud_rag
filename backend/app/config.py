"""Application configuration management."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "LLM Test Platform"
    debug: bool = False

    # Database
    database_url: str = "postgresql://admin:password@localhost:5432/llm_platform"

    # Security
    secret_key: str = "your-secret-key-here-min-32-chars-CHANGE-THIS"
    encryption_key: str = "your-fernet-encryption-key-CHANGE-THIS"

    # JWT
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/v1/auth/google/callback"

    # Admin
    admin_emails: str = ""  # Comma-separated list

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @property
    def admin_email_list(self) -> list[str]:
        """Parse admin emails into a list."""
        if not self.admin_emails:
            return []
        return [email.strip() for email in self.admin_emails.split(",")]

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
