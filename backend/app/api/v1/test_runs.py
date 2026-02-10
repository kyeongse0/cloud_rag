"""Test Runs API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import ActiveUser
from app.db.session import get_db
from app.models.model import Model
from app.schemas.test_run import (
    TestRunCreate,
    TestRunListSummaryResponse,
    TestRunResponse,
    TestRunSummary,
    TestResultResponse,
)
from app.services.test_run import TestRunService

router = APIRouter()


@router.post(
    "",
    response_model=TestRunResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_test_run(
    test_data: TestRunCreate,
    current_user: ActiveUser,
    db: AsyncSession = Depends(get_db),
) -> TestRunResponse:
    """
    Create and execute a new test run.

    Tests the user message against all specified models concurrently
    and returns the results.
    """
    service = TestRunService(db)
    test_run = await service.create_and_execute_test(current_user.id, test_data)

    # Build response with model names
    results = []
    for result in test_run.results:
        # Get model name
        model = await db.get(Model, result.model_id)
        model_name = model.name if model else "Unknown"

        results.append(
            TestResultResponse(
                id=result.id,
                model_id=result.model_id,
                model_name=model_name,
                parameters=result.parameters,
                response=result.response,
                latency_ms=result.latency_ms,
                token_count=result.token_count,
                error=result.error,
                created_at=result.created_at,
            )
        )

    return TestRunResponse(
        id=test_run.id,
        user_id=test_run.user_id,
        prompt_template_id=test_run.prompt_template_id,
        user_message=test_run.user_message,
        system_prompt=test_run.system_prompt,
        results=results,
        created_at=test_run.created_at,
        updated_at=test_run.updated_at,
    )


@router.get("", response_model=TestRunListSummaryResponse)
async def get_test_runs(
    current_user: ActiveUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> TestRunListSummaryResponse:
    """Get paginated list of test runs for the current user."""
    service = TestRunService(db)
    test_runs, total = await service.get_test_runs(
        user_id=current_user.id, skip=skip, limit=limit
    )

    items = [
        TestRunSummary(
            id=run.id,
            user_message=run.user_message,
            system_prompt=run.system_prompt,
            prompt_template_id=run.prompt_template_id,
            result_count=len(run.results),
            created_at=run.created_at,
        )
        for run in test_runs
    ]

    return TestRunListSummaryResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{test_run_id}", response_model=TestRunResponse)
async def get_test_run(
    test_run_id: UUID,
    current_user: ActiveUser,
    db: AsyncSession = Depends(get_db),
) -> TestRunResponse:
    """Get a specific test run with all results."""
    service = TestRunService(db)
    test_run = await service.get_test_run_by_id(test_run_id, current_user.id)

    if not test_run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test run not found",
        )

    # Build response with model names
    results = []
    for result in test_run.results:
        model = await db.get(Model, result.model_id)
        model_name = model.name if model else "Unknown"

        results.append(
            TestResultResponse(
                id=result.id,
                model_id=result.model_id,
                model_name=model_name,
                parameters=result.parameters,
                response=result.response,
                latency_ms=result.latency_ms,
                token_count=result.token_count,
                error=result.error,
                created_at=result.created_at,
            )
        )

    return TestRunResponse(
        id=test_run.id,
        user_id=test_run.user_id,
        prompt_template_id=test_run.prompt_template_id,
        user_message=test_run.user_message,
        system_prompt=test_run.system_prompt,
        results=results,
        created_at=test_run.created_at,
        updated_at=test_run.updated_at,
    )


@router.delete("/{test_run_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_run(
    test_run_id: UUID,
    current_user: ActiveUser,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a test run and all its results."""
    service = TestRunService(db)
    success = await service.delete_test_run(test_run_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test run not found",
        )
