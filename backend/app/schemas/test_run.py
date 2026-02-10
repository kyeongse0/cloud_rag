"""Test Run and Test Result schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ModelTestConfig(BaseModel):
    """Configuration for testing a single model."""

    model_id: UUID
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, ge=1, le=4096)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)


class TestRunCreate(BaseModel):
    """Schema for creating a new test run."""

    user_message: str = Field(..., min_length=1, max_length=10000)
    system_prompt: str | None = Field(default=None, max_length=10000)
    prompt_template_id: UUID | None = None
    models: list[ModelTestConfig] = Field(..., min_length=1, max_length=10)


class TestResultResponse(BaseModel):
    """Schema for test result response."""

    id: UUID
    model_id: UUID
    model_name: str
    parameters: dict
    response: str | None
    latency_ms: int | None
    token_count: int | None
    error: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TestRunResponse(BaseModel):
    """Schema for test run response."""

    id: UUID
    user_id: UUID
    prompt_template_id: UUID | None
    user_message: str
    system_prompt: str | None
    results: list[TestResultResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TestRunListResponse(BaseModel):
    """Schema for paginated test run list."""

    items: list[TestRunResponse]
    total: int
    skip: int
    limit: int


class TestRunSummary(BaseModel):
    """Schema for test run summary (without full results)."""

    id: UUID
    user_message: str
    system_prompt: str | None
    prompt_template_id: UUID | None
    result_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TestRunListSummaryResponse(BaseModel):
    """Schema for paginated test run summary list."""

    items: list[TestRunSummary]
    total: int
    skip: int
    limit: int
