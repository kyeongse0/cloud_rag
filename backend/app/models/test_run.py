"""Test Run and Test Result models."""

import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class TestRun(Base, UUIDMixin, TimestampMixin):
    """A single test execution session."""

    __tablename__ = "test_runs"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    prompt_template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("prompt_templates.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="test_runs")
    prompt_template: Mapped["PromptTemplate | None"] = relationship(
        "PromptTemplate", back_populates="test_runs"
    )
    results: Mapped[list["TestResult"]] = relationship(
        "TestResult", back_populates="test_run", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TestRun {self.id}>"


class TestResult(Base, UUIDMixin, TimestampMixin):
    """Result from a single model within a test run."""

    __tablename__ = "test_results"

    test_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("test_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    model_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("models.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    parameters: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )  # {temperature, max_tokens, top_p}
    response: Mapped[str | None] = mapped_column(Text, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    test_run: Mapped["TestRun"] = relationship("TestRun", back_populates="results")
    model: Mapped["Model"] = relationship("Model", back_populates="test_results")

    def __repr__(self) -> str:
        return f"<TestResult {self.id}>"


# Avoid circular imports
from app.models.user import User
from app.models.prompt import PromptTemplate
from app.models.model import Model
