"""Prompt Template and Version models."""

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class PromptTemplate(Base, UUIDMixin, TimestampMixin):
    """Reusable system prompt template."""

    __tablename__ = "prompt_templates"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="prompt_templates")
    versions: Mapped[list["PromptVersion"]] = relationship(
        "PromptVersion", back_populates="prompt", cascade="all, delete-orphan"
    )
    test_runs: Mapped[list["TestRun"]] = relationship(
        "TestRun", back_populates="prompt_template"
    )

    def __repr__(self) -> str:
        return f"<PromptTemplate {self.name}>"


class PromptVersion(Base, UUIDMixin):
    """Version history for prompt templates."""

    __tablename__ = "prompt_versions"

    prompt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("prompt_templates.id", ondelete="CASCADE"),
        nullable=False,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(
        String, server_default="now()", nullable=False
    )

    # Relationships
    prompt: Mapped["PromptTemplate"] = relationship(
        "PromptTemplate", back_populates="versions"
    )

    __table_args__ = (
        # Unique constraint on prompt_id + version_number
        {"sqlite_autoincrement": True},
    )

    def __repr__(self) -> str:
        return f"<PromptVersion {self.prompt_id}:v{self.version_number}>"


# Avoid circular imports
from app.models.user import User
from app.models.test_run import TestRun
