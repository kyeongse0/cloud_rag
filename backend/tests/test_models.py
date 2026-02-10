"""Tests for model management."""

from uuid import uuid4

import pytest

from app.models.model import Model
from app.schemas.model import ModelCreate, ModelUpdate
from app.services.model import ModelService


class TestModelService:
    """Tests for ModelService."""

    @pytest.mark.asyncio
    async def test_create_model(self, db_session):
        """Test model creation."""
        model_service = ModelService(db_session)

        model_data = ModelCreate(
            name="Test Model",
            endpoint_url="http://localhost:8000",
            api_key="test-api-key",
            metadata_={"max_tokens": 4096},
        )

        model = await model_service.create_model(model_data)

        assert model is not None
        assert model.name == "Test Model"
        assert model.endpoint_url == "http://localhost:8000"
        assert model.is_active is True

    @pytest.mark.asyncio
    async def test_get_model_by_id(self, db_session):
        """Test getting model by ID."""
        # Create a model first
        model = Model(
            name="Test Model",
            endpoint_url="http://localhost:8000",
            is_active=True,
        )
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)

        model_service = ModelService(db_session)
        fetched = await model_service.get_model_by_id(model.id)

        assert fetched is not None
        assert fetched.id == model.id

    @pytest.mark.asyncio
    async def test_get_model_by_name(self, db_session):
        """Test getting model by name."""
        model = Model(
            name="Unique Model Name",
            endpoint_url="http://localhost:8000",
            is_active=True,
        )
        db_session.add(model)
        await db_session.commit()

        model_service = ModelService(db_session)
        fetched = await model_service.get_model_by_name("Unique Model Name")

        assert fetched is not None
        assert fetched.name == "Unique Model Name"

    @pytest.mark.asyncio
    async def test_get_models_pagination(self, db_session):
        """Test paginated model listing."""
        # Create multiple models
        for i in range(5):
            model = Model(
                name=f"Model {i}",
                endpoint_url=f"http://localhost:800{i}",
                is_active=True,
            )
            db_session.add(model)
        await db_session.commit()

        model_service = ModelService(db_session)
        models, total = await model_service.get_models(skip=0, limit=3)

        assert len(models) == 3
        assert total == 5

    @pytest.mark.asyncio
    async def test_update_model(self, db_session):
        """Test model update."""
        model = Model(
            name="Original Name",
            endpoint_url="http://localhost:8000",
            is_active=True,
        )
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)

        model_service = ModelService(db_session)
        update_data = ModelUpdate(name="Updated Name")
        updated = await model_service.update_model(model.id, update_data)

        assert updated is not None
        assert updated.name == "Updated Name"

    @pytest.mark.asyncio
    async def test_delete_model_soft(self, db_session):
        """Test soft delete (deactivation)."""
        model = Model(
            name="To Delete",
            endpoint_url="http://localhost:8000",
            is_active=True,
        )
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)

        model_service = ModelService(db_session)
        success = await model_service.delete_model(model.id)

        assert success is True

        # Model should still exist but be inactive
        fetched = await model_service.get_model_by_id(model.id)
        assert fetched is not None
        assert fetched.is_active is False

    @pytest.mark.asyncio
    async def test_get_models_active_only(self, db_session):
        """Test filtering active models only."""
        # Create active and inactive models
        active_model = Model(
            name="Active Model",
            endpoint_url="http://localhost:8000",
            is_active=True,
        )
        inactive_model = Model(
            name="Inactive Model",
            endpoint_url="http://localhost:8001",
            is_active=False,
        )
        db_session.add(active_model)
        db_session.add(inactive_model)
        await db_session.commit()

        model_service = ModelService(db_session)

        # Get active only
        models, total = await model_service.get_models(active_only=True)
        assert total == 1
        assert models[0].name == "Active Model"

        # Get all
        models, total = await model_service.get_models(active_only=False)
        assert total == 2
