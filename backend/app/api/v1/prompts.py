"""Prompt management API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import ActiveUser, DBSession
from app.schemas.prompt import (
    PromptCreate,
    PromptListResponse,
    PromptResponse,
    PromptRollbackRequest,
    PromptUpdate,
    PromptVersionListResponse,
    PromptVersionResponse,
    PromptWithVersions,
)
from app.services.prompt import PromptService

router = APIRouter()


def get_prompt_service(db: DBSession) -> PromptService:
    """Dependency for prompt service."""
    return PromptService(db)


@router.get("", response_model=PromptListResponse)
async def list_prompts(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    tags: list[str] | None = Query(None, description="Filter by tags"),
    favorites_only: bool = Query(False, description="Only show favorites"),
    current_user: ActiveUser = None,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Get paginated list of prompts for current user."""
    skip = (page - 1) * size
    prompts, total = await prompt_service.get_prompts(
        user_id=current_user.id,
        skip=skip,
        limit=size,
        tags=tags,
        favorites_only=favorites_only,
    )

    return PromptListResponse(
        items=[PromptResponse.model_validate(p) for p in prompts],
        total=total,
        page=page,
        size=size,
    )


@router.post("", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    prompt_data: PromptCreate,
    current_user: ActiveUser = None,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Create a new prompt."""
    prompt = await prompt_service.create_prompt(current_user.id, prompt_data)
    return PromptResponse.model_validate(prompt)


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: UUID,
    current_user: ActiveUser = None,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Get prompt by ID."""
    prompt = await prompt_service.get_prompt_by_id(prompt_id, current_user.id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found",
        )
    return PromptResponse.model_validate(prompt)


@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: UUID,
    prompt_data: PromptUpdate,
    current_user: ActiveUser = None,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Update a prompt. Creates a new version if content changes."""
    prompt = await prompt_service.update_prompt(prompt_id, current_user.id, prompt_data)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found",
        )
    return PromptResponse.model_validate(prompt)


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: UUID,
    current_user: ActiveUser = None,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Delete a prompt and all its versions."""
    success = await prompt_service.delete_prompt(prompt_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found",
        )
    return None


@router.post("/{prompt_id}/favorite", response_model=PromptResponse)
async def toggle_favorite(
    prompt_id: UUID,
    current_user: ActiveUser = None,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Toggle favorite status of a prompt."""
    prompt = await prompt_service.toggle_favorite(prompt_id, current_user.id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found",
        )
    return PromptResponse.model_validate(prompt)


@router.get("/{prompt_id}/versions", response_model=PromptVersionListResponse)
async def get_prompt_versions(
    prompt_id: UUID,
    current_user: ActiveUser = None,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Get version history of a prompt."""
    versions = await prompt_service.get_versions(prompt_id, current_user.id)
    if not versions:
        # Check if prompt exists
        prompt = await prompt_service.get_prompt_by_id(prompt_id, current_user.id)
        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prompt not found",
            )

    return PromptVersionListResponse(
        items=[PromptVersionResponse.model_validate(v) for v in versions],
        total=len(versions),
    )


@router.post("/{prompt_id}/rollback", response_model=PromptResponse)
async def rollback_prompt(
    prompt_id: UUID,
    rollback_data: PromptRollbackRequest,
    current_user: ActiveUser = None,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """Rollback prompt content to a specific version."""
    prompt = await prompt_service.rollback_to_version(
        prompt_id, current_user.id, rollback_data.version_number
    )
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt or version not found",
        )
    return PromptResponse.model_validate(prompt)
