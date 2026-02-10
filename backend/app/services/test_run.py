"""Test Run service for executing tests against LLM models."""

import asyncio
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.model import Model
from app.models.test_run import TestResult, TestRun
from app.schemas.test_run import ModelTestConfig, TestRunCreate
from app.utils.llm_client import llm_client


class TestRunService:
    """Service for managing test runs and executions."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_and_execute_test(
        self, user_id: UUID, test_data: TestRunCreate
    ) -> TestRun:
        """
        Create a new test run and execute it against specified models.

        Args:
            user_id: ID of the user creating the test
            test_data: Test configuration including message and model configs

        Returns:
            TestRun with all results populated
        """
        # Create the test run
        test_run = TestRun(
            user_id=user_id,
            user_message=test_data.user_message,
            system_prompt=test_data.system_prompt,
            prompt_template_id=test_data.prompt_template_id,
        )
        self.db.add(test_run)
        await self.db.flush()

        # Fetch all requested models
        model_ids = [config.model_id for config in test_data.models]
        result = await self.db.execute(
            select(Model).where(Model.id.in_(model_ids), Model.is_active == True)
        )
        models = {m.id: m for m in result.scalars().all()}

        # Create tasks for concurrent model calls
        tasks = []
        for config in test_data.models:
            model = models.get(config.model_id)
            if model:
                task = self._execute_single_model(
                    test_run.id,
                    model,
                    test_data.user_message,
                    test_data.system_prompt,
                    config,
                )
                tasks.append(task)

        # Execute all model calls concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Add results to session
        for result in results:
            if isinstance(result, TestResult):
                self.db.add(result)

        await self.db.commit()

        # Refresh with relationships
        await self.db.refresh(test_run, ["results"])
        return test_run

    async def _execute_single_model(
        self,
        test_run_id: UUID,
        model: Model,
        user_message: str,
        system_prompt: str | None,
        config: ModelTestConfig,
    ) -> TestResult:
        """Execute a single model test and return the result."""
        response = await llm_client.chat_completion(
            endpoint_url=model.endpoint_url,
            api_key=model.api_key,
            model_name=model.model_name or model.name,
            user_message=user_message,
            system_prompt=system_prompt,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p,
        )

        return TestResult(
            test_run_id=test_run_id,
            model_id=model.id,
            parameters={
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "top_p": config.top_p,
            },
            response=response.content,
            latency_ms=response.latency_ms,
            token_count=response.token_count,
            error=response.error,
        )

    async def get_test_run_by_id(
        self, test_run_id: UUID, user_id: UUID
    ) -> TestRun | None:
        """Get a test run by ID with all results."""
        result = await self.db.execute(
            select(TestRun)
            .options(selectinload(TestRun.results))
            .where(TestRun.id == test_run_id, TestRun.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_test_runs(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[TestRun], int]:
        """Get paginated list of test runs for a user."""
        # Count query
        count_result = await self.db.execute(
            select(func.count(TestRun.id)).where(TestRun.user_id == user_id)
        )
        total = count_result.scalar() or 0

        # Main query
        result = await self.db.execute(
            select(TestRun)
            .options(selectinload(TestRun.results))
            .where(TestRun.user_id == user_id)
            .order_by(TestRun.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        test_runs = list(result.scalars().all())

        return test_runs, total

    async def delete_test_run(self, test_run_id: UUID, user_id: UUID) -> bool:
        """Delete a test run and all its results."""
        result = await self.db.execute(
            select(TestRun).where(
                TestRun.id == test_run_id, TestRun.user_id == user_id
            )
        )
        test_run = result.scalar_one_or_none()

        if not test_run:
            return False

        await self.db.delete(test_run)
        await self.db.commit()
        return True
