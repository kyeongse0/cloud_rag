"""Prompt Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PromptBase(BaseModel):
    """Base prompt schema."""

    name: str
    description: str | None = None
    content: str
    tags: list[str] | None = None


class PromptCreate(PromptBase):
    """Schema for creating a prompt."""

    pass


class PromptUpdate(BaseModel):
    """Schema for updating a prompt."""

    name: str | None = None
    description: str | None = None
    content: str | None = None
    is_favorite: bool | None = None
    tags: list[str] | None = None


class PromptResponse(PromptBase):
    """Schema for prompt response."""

    id: UUID
    user_id: UUID
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PromptListResponse(BaseModel):
    """Schema for paginated prompt list."""

    items: list[PromptResponse]
    total: int
    page: int
    size: int


# Version schemas
class PromptVersionResponse(BaseModel):
    """Schema for prompt version response."""

    id: UUID
    prompt_id: UUID
    version_number: int
    content: str
    created_at: str

    model_config = {"from_attributes": True}


class PromptVersionListResponse(BaseModel):
    """Schema for prompt version list."""

    items: list[PromptVersionResponse]
    total: int


class PromptWithVersions(PromptResponse):
    """Schema for prompt with version history."""

    versions: list[PromptVersionResponse] = []


class PromptRollbackRequest(BaseModel):
    """Schema for rollback request."""

    version_number: int
