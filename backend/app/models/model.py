"""LLM Model model."""

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class Model(Base, UUIDMixin, TimestampMixin):
    """LLM Model configuration."""

    __tablename__ = "models"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    endpoint_url: Mapped[str] = mapped_column(String(512), nullable=False)
    api_key: Mapped[str | None] = mapped_column(Text, nullable=True)  # Encrypted
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    metadata_: Mapped[dict | None] = mapped_column(
        "metadata", JSONB, nullable=True
    )  # {max_tokens, context_length, model_type}

    # Relationships
    test_results: Mapped[list["TestResult"]] = relationship(
        "TestResult", back_populates="model", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Model {self.name}>"


# Avoid circular imports
from app.models.test_run import TestResult
