"""Tests for test run execution."""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.models.model import Model
from app.models.test_run import TestRun, TestResult
from app.schemas.test_run import ModelTestConfig, TestRunCreate
from app.services.test_run import TestRunService
from app.utils.llm_client import LLMResponse


class TestTestRunService:
    """Tests for TestRunService."""

    @pytest.fixture
    async def test_model(self, db_session):
        """Create a test model."""
        model = Model(
            name="Test LLM",
            model_name="test-model",
            endpoint_url="http://localhost:8000",
            api_key="test-key",
            is_active=True,
        )
        db_session.add(model)
        await db_session.commit()
        await db_session.refresh(model)
        return model

    @pytest.fixture
    async def test_models(self, db_session):
        """Create multiple test models."""
        models = []
        for i in range(3):
            model = Model(
                name=f"Test LLM {i}",
                model_name=f"test-model-{i}",
                endpoint_url=f"http://localhost:800{i}",
                is_active=True,
            )
            db_session.add(model)
            models.append(model)
        await db_session.commit()
        for model in models:
            await db_session.refresh(model)
        return models

    @pytest.mark.asyncio
    async def test_create_and_execute_test(self, db_session, test_user, test_model):
        """Test creating and executing a test run."""
        mock_response = LLMResponse(
            content="Hello! I'm a helpful assistant.",
            latency_ms=150,
            token_count=10,
            error=None,
        )

        with patch(
            "app.services.test_run.llm_client.chat_completion",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            service = TestRunService(db_session)

            test_data = TestRunCreate(
                user_message="Hello, how are you?",
                system_prompt="You are a helpful assistant.",
                models=[
                    ModelTestConfig(
                        model_id=test_model.id,
                        temperature=0.7,
                        max_tokens=512,
                    )
                ],
            )

            test_run = await service.create_and_execute_test(test_user.id, test_data)

            assert test_run is not None
            assert test_run.user_id == test_user.id
            assert test_run.user_message == "Hello, how are you?"
            assert test_run.system_prompt == "You are a helpful assistant."
            assert len(test_run.results) == 1

            result = test_run.results[0]
            assert result.model_id == test_model.id
            assert result.response == "Hello! I'm a helpful assistant."
            assert result.latency_ms == 150
            assert result.token_count == 10
            assert result.error is None

    @pytest.mark.asyncio
    async def test_execute_multiple_models(self, db_session, test_user, test_models):
        """Test executing against multiple models concurrently."""
        mock_response = LLMResponse(
            content="Test response",
            latency_ms=100,
            token_count=5,
            error=None,
        )

        with patch(
            "app.services.test_run.llm_client.chat_completion",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            service = TestRunService(db_session)

            test_data = TestRunCreate(
                user_message="Test message",
                models=[
                    ModelTestConfig(model_id=model.id) for model in test_models
                ],
            )

            test_run = await service.create_and_execute_test(test_user.id, test_data)

            assert len(test_run.results) == 3
            for result in test_run.results:
                assert result.response == "Test response"

    @pytest.mark.asyncio
    async def test_execute_with_error(self, db_session, test_user, test_model):
        """Test handling model errors."""
        mock_response = LLMResponse(
            content=None,
            latency_ms=50,
            token_count=None,
            error="Connection refused",
        )

        with patch(
            "app.services.test_run.llm_client.chat_completion",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            service = TestRunService(db_session)

            test_data = TestRunCreate(
                user_message="Test message",
                models=[ModelTestConfig(model_id=test_model.id)],
            )

            test_run = await service.create_and_execute_test(test_user.id, test_data)

            assert len(test_run.results) == 1
            result = test_run.results[0]
            assert result.response is None
            assert result.error == "Connection refused"

    @pytest.mark.asyncio
    async def test_get_test_run_by_id(self, db_session, test_user, test_model):
        """Test getting test run by ID."""
        # Create a test run directly
        test_run = TestRun(
            user_id=test_user.id,
            user_message="Test message",
        )
        db_session.add(test_run)
        await db_session.flush()

        result = TestResult(
            test_run_id=test_run.id,
            model_id=test_model.id,
            parameters={"temperature": 0.7},
            response="Test response",
            latency_ms=100,
        )
        db_session.add(result)
        await db_session.commit()

        service = TestRunService(db_session)
        fetched = await service.get_test_run_by_id(test_run.id, test_user.id)

        assert fetched is not None
        assert fetched.id == test_run.id
        assert len(fetched.results) == 1

    @pytest.mark.asyncio
    async def test_get_test_run_wrong_user(self, db_session, test_user):
        """Test that users can't access other users' test runs."""
        test_run = TestRun(
            user_id=test_user.id,
            user_message="Test message",
        )
        db_session.add(test_run)
        await db_session.commit()

        service = TestRunService(db_session)
        other_user_id = uuid4()
        fetched = await service.get_test_run_by_id(test_run.id, other_user_id)

        assert fetched is None

    @pytest.mark.asyncio
    async def test_get_test_runs_pagination(self, db_session, test_user):
        """Test paginated test run listing."""
        for i in range(5):
            test_run = TestRun(
                user_id=test_user.id,
                user_message=f"Message {i}",
            )
            db_session.add(test_run)
        await db_session.commit()

        service = TestRunService(db_session)
        test_runs, total = await service.get_test_runs(
            user_id=test_user.id, skip=0, limit=3
        )

        assert len(test_runs) == 3
        assert total == 5

    @pytest.mark.asyncio
    async def test_delete_test_run(self, db_session, test_user, test_model):
        """Test deleting a test run."""
        test_run = TestRun(
            user_id=test_user.id,
            user_message="To delete",
        )
        db_session.add(test_run)
        await db_session.flush()

        result = TestResult(
            test_run_id=test_run.id,
            model_id=test_model.id,
            parameters={},
            response="Response",
        )
        db_session.add(result)
        await db_session.commit()
        await db_session.refresh(test_run)

        service = TestRunService(db_session)
        success = await service.delete_test_run(test_run.id, test_user.id)

        assert success is True

        # Verify deletion
        fetched = await service.get_test_run_by_id(test_run.id, test_user.id)
        assert fetched is None

    @pytest.mark.asyncio
    async def test_skip_inactive_models(self, db_session, test_user):
        """Test that inactive models are skipped."""
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
        await db_session.refresh(active_model)
        await db_session.refresh(inactive_model)

        mock_response = LLMResponse(
            content="Response",
            latency_ms=100,
            token_count=5,
            error=None,
        )

        with patch(
            "app.services.test_run.llm_client.chat_completion",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            service = TestRunService(db_session)

            test_data = TestRunCreate(
                user_message="Test",
                models=[
                    ModelTestConfig(model_id=active_model.id),
                    ModelTestConfig(model_id=inactive_model.id),
                ],
            )

            test_run = await service.create_and_execute_test(test_user.id, test_data)

            # Only active model should have a result
            assert len(test_run.results) == 1
            assert test_run.results[0].model_id == active_model.id
