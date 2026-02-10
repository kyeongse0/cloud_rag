"""Model management service."""

import time
from uuid import UUID

import httpx
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.model import Model
from app.schemas.model import ModelCreate, ModelHealthCheck, ModelUpdate


class ModelService:
    """Service for model management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_model_by_id(self, model_id: UUID) -> Model | None:
        """Get model by ID."""
        result = await self.db.execute(select(Model).where(Model.id == model_id))
        return result.scalar_one_or_none()

    async def get_model_by_name(self, name: str) -> Model | None:
        """Get model by name."""
        result = await self.db.execute(select(Model).where(Model.name == name))
        return result.scalar_one_or_none()

    async def get_models(
        self,
        skip: int = 0,
        limit: int = 20,
        active_only: bool = True,
    ) -> tuple[list[Model], int]:
        """Get paginated list of models."""
        query = select(Model)
        count_query = select(func.count(Model.id))

        if active_only:
            query = query.where(Model.is_active == True)
            count_query = count_query.where(Model.is_active == True)

        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Model.created_at.desc())
        result = await self.db.execute(query)
        models = list(result.scalars().all())

        return models, total

    async def create_model(self, model_data: ModelCreate) -> Model:
        """Create a new model."""
        model = Model(
            name=model_data.name,
            endpoint_url=model_data.endpoint_url,
            api_key=model_data.api_key,  # TODO: Encrypt before storing
            metadata_=model_data.metadata_,
        )
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return model

    async def update_model(
        self, model_id: UUID, model_data: ModelUpdate
    ) -> Model | None:
        """Update an existing model."""
        model = await self.get_model_by_id(model_id)
        if not model:
            return None

        update_data = model_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)

        await self.db.flush()
        await self.db.refresh(model)
        return model

    async def delete_model(self, model_id: UUID) -> bool:
        """Soft delete a model (set is_active to False)."""
        model = await self.get_model_by_id(model_id)
        if not model:
            return False

        model.is_active = False
        await self.db.flush()
        return True

    async def hard_delete_model(self, model_id: UUID) -> bool:
        """Permanently delete a model."""
        model = await self.get_model_by_id(model_id)
        if not model:
            return False

        await self.db.delete(model)
        await self.db.flush()
        return True

    async def health_check(self, model_id: UUID) -> ModelHealthCheck:
        """Check if a model endpoint is healthy."""
        model = await self.get_model_by_id(model_id)
        if not model:
            return ModelHealthCheck(
                model_id=model_id,
                model_name="Unknown",
                endpoint_url="",
                is_healthy=False,
                error="Model not found",
            )

        start_time = time.time()
        is_healthy = False
        error = None
        latency_ms = None

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Try to hit the models endpoint (OpenAI-compatible)
                headers = {}
                if model.api_key:
                    headers["Authorization"] = f"Bearer {model.api_key}"

                response = await client.get(
                    f"{model.endpoint_url}/v1/models",
                    headers=headers,
                )

                latency_ms = int((time.time() - start_time) * 1000)

                if response.status_code == 200:
                    is_healthy = True
                else:
                    error = f"HTTP {response.status_code}: {response.text[:200]}"

        except httpx.TimeoutException:
            latency_ms = int((time.time() - start_time) * 1000)
            error = "Connection timeout"
        except httpx.ConnectError:
            error = "Connection refused"
        except Exception as e:
            error = str(e)

        return ModelHealthCheck(
            model_id=model.id,
            model_name=model.name,
            endpoint_url=model.endpoint_url,
            is_healthy=is_healthy,
            latency_ms=latency_ms,
            error=error,
        )
