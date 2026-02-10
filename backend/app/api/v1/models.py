"""Model management API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import ActiveUser, DBSession
from app.schemas.model import (
    ModelCreate,
    ModelHealthCheck,
    ModelListResponse,
    ModelResponse,
    ModelUpdate,
)
from app.services.model import ModelService

router = APIRouter()


def get_model_service(db: DBSession) -> ModelService:
    """Dependency for model service."""
    return ModelService(db)


@router.get("", response_model=ModelListResponse)
async def list_models(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    active_only: bool = Query(True, description="Only show active models"),
    current_user: ActiveUser = None,
    model_service: ModelService = Depends(get_model_service),
):
    """Get paginated list of models."""
    skip = (page - 1) * size
    models, total = await model_service.get_models(
        skip=skip, limit=size, active_only=active_only
    )

    return ModelListResponse(
        items=[ModelResponse.model_validate(m) for m in models],
        total=total,
        page=page,
        size=size,
    )


@router.post("", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    model_data: ModelCreate,
    current_user: ActiveUser = None,
    model_service: ModelService = Depends(get_model_service),
):
    """Create a new model."""
    # Check if model with same name exists
    existing = await model_service.get_model_by_name(model_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Model with name '{model_data.name}' already exists",
        )

    model = await model_service.create_model(model_data)
    return ModelResponse.model_validate(model)


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: UUID,
    current_user: ActiveUser = None,
    model_service: ModelService = Depends(get_model_service),
):
    """Get model by ID."""
    model = await model_service.get_model_by_id(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
    return ModelResponse.model_validate(model)


@router.put("/{model_id}", response_model=ModelResponse)
async def update_model(
    model_id: UUID,
    model_data: ModelUpdate,
    current_user: ActiveUser = None,
    model_service: ModelService = Depends(get_model_service),
):
    """Update a model."""
    model = await model_service.update_model(model_id, model_data)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
    return ModelResponse.model_validate(model)


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(
    model_id: UUID,
    current_user: ActiveUser = None,
    model_service: ModelService = Depends(get_model_service),
):
    """Soft delete a model (deactivate)."""
    success = await model_service.delete_model(model_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
    return None


@router.post("/{model_id}/health", response_model=ModelHealthCheck)
async def check_model_health(
    model_id: UUID,
    current_user: ActiveUser = None,
    model_service: ModelService = Depends(get_model_service),
):
    """Check if model endpoint is healthy."""
    result = await model_service.health_check(model_id)
    if result.error == "Model not found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
    return result
