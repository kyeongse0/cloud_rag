"""Model Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class ModelBase(BaseModel):
    """Base model schema."""

    name: str
    endpoint_url: str
    api_key: str | None = None
    metadata_: dict | None = None


class ModelCreate(ModelBase):
    """Schema for creating a model."""

    pass


class ModelUpdate(BaseModel):
    """Schema for updating a model."""

    name: str | None = None
    endpoint_url: str | None = None
    api_key: str | None = None
    is_active: bool | None = None
    metadata_: dict | None = None


class ModelResponse(BaseModel):
    """Schema for model response."""

    id: UUID
    name: str
    endpoint_url: str
    is_active: bool
    metadata_: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ModelWithApiKey(ModelResponse):
    """Schema for model with API key (admin only)."""

    api_key: str | None = None


class ModelHealthCheck(BaseModel):
    """Schema for model health check response."""

    model_id: UUID
    model_name: str
    endpoint_url: str
    is_healthy: bool
    latency_ms: int | None = None
    error: str | None = None


class ModelListResponse(BaseModel):
    """Schema for paginated model list."""

    items: list[ModelResponse]
    total: int
    page: int
    size: int
