"""Tests for prompt management."""

from uuid import uuid4

import pytest

from app.models.prompt import PromptTemplate, PromptVersion
from app.schemas.prompt import PromptCreate, PromptUpdate
from app.services.prompt import PromptService


class TestPromptService:
    """Tests for PromptService."""

    @pytest.mark.asyncio
    async def test_create_prompt(self, db_session, test_user):
        """Test prompt creation with initial version."""
        prompt_service = PromptService(db_session)

        prompt_data = PromptCreate(
            name="Test Prompt",
            description="A test prompt",
            content="You are a helpful assistant.",
            tags=["test", "assistant"],
        )

        prompt = await prompt_service.create_prompt(test_user.id, prompt_data)

        assert prompt is not None
        assert prompt.name == "Test Prompt"
        assert prompt.content == "You are a helpful assistant."
        assert prompt.user_id == test_user.id

    @pytest.mark.asyncio
    async def test_get_prompt_by_id(self, db_session, test_user):
        """Test getting prompt by ID."""
        prompt = PromptTemplate(
            user_id=test_user.id,
            name="Test Prompt",
            content="Test content",
        )
        db_session.add(prompt)
        await db_session.commit()
        await db_session.refresh(prompt)

        prompt_service = PromptService(db_session)
        fetched = await prompt_service.get_prompt_by_id(prompt.id, test_user.id)

        assert fetched is not None
        assert fetched.id == prompt.id

    @pytest.mark.asyncio
    async def test_get_prompt_wrong_user(self, db_session, test_user):
        """Test that users can't access other users' prompts."""
        prompt = PromptTemplate(
            user_id=test_user.id,
            name="Test Prompt",
            content="Test content",
        )
        db_session.add(prompt)
        await db_session.commit()

        prompt_service = PromptService(db_session)
        other_user_id = uuid4()
        fetched = await prompt_service.get_prompt_by_id(prompt.id, other_user_id)

        assert fetched is None

    @pytest.mark.asyncio
    async def test_get_prompts_pagination(self, db_session, test_user):
        """Test paginated prompt listing."""
        for i in range(5):
            prompt = PromptTemplate(
                user_id=test_user.id,
                name=f"Prompt {i}",
                content=f"Content {i}",
            )
            db_session.add(prompt)
        await db_session.commit()

        prompt_service = PromptService(db_session)
        prompts, total = await prompt_service.get_prompts(
            user_id=test_user.id, skip=0, limit=3
        )

        assert len(prompts) == 3
        assert total == 5

    @pytest.mark.asyncio
    async def test_get_prompts_favorites_only(self, db_session, test_user):
        """Test filtering favorites only."""
        favorite = PromptTemplate(
            user_id=test_user.id,
            name="Favorite",
            content="Favorite content",
            is_favorite=True,
        )
        regular = PromptTemplate(
            user_id=test_user.id,
            name="Regular",
            content="Regular content",
            is_favorite=False,
        )
        db_session.add(favorite)
        db_session.add(regular)
        await db_session.commit()

        prompt_service = PromptService(db_session)
        prompts, total = await prompt_service.get_prompts(
            user_id=test_user.id, favorites_only=True
        )

        assert total == 1
        assert prompts[0].name == "Favorite"

    @pytest.mark.asyncio
    async def test_update_prompt_creates_version(self, db_session, test_user):
        """Test that updating content creates a new version."""
        prompt_service = PromptService(db_session)

        # Create prompt
        prompt_data = PromptCreate(
            name="Versioned Prompt",
            content="Version 1 content",
        )
        prompt = await prompt_service.create_prompt(test_user.id, prompt_data)

        # Update content
        update_data = PromptUpdate(content="Version 2 content")
        updated = await prompt_service.update_prompt(
            prompt.id, test_user.id, update_data
        )

        assert updated is not None
        assert updated.content == "Version 2 content"

        # Check versions
        versions = await prompt_service.get_versions(prompt.id, test_user.id)
        assert len(versions) == 2

    @pytest.mark.asyncio
    async def test_toggle_favorite(self, db_session, test_user):
        """Test toggling favorite status."""
        prompt = PromptTemplate(
            user_id=test_user.id,
            name="Test",
            content="Test",
            is_favorite=False,
        )
        db_session.add(prompt)
        await db_session.commit()
        await db_session.refresh(prompt)

        prompt_service = PromptService(db_session)

        # Toggle to favorite
        toggled = await prompt_service.toggle_favorite(prompt.id, test_user.id)
        assert toggled.is_favorite is True

        # Toggle back
        toggled = await prompt_service.toggle_favorite(prompt.id, test_user.id)
        assert toggled.is_favorite is False

    @pytest.mark.asyncio
    async def test_delete_prompt(self, db_session, test_user):
        """Test prompt deletion."""
        prompt = PromptTemplate(
            user_id=test_user.id,
            name="To Delete",
            content="Delete me",
        )
        db_session.add(prompt)
        await db_session.commit()
        await db_session.refresh(prompt)

        prompt_service = PromptService(db_session)
        success = await prompt_service.delete_prompt(prompt.id, test_user.id)

        assert success is True

        # Verify deletion
        fetched = await prompt_service.get_prompt_by_id(prompt.id, test_user.id)
        assert fetched is None

    @pytest.mark.asyncio
    async def test_rollback_to_version(self, db_session, test_user):
        """Test rolling back to a previous version."""
        prompt_service = PromptService(db_session)

        # Create and update prompt
        prompt_data = PromptCreate(name="Rollback Test", content="Original")
        prompt = await prompt_service.create_prompt(test_user.id, prompt_data)

        await prompt_service.update_prompt(
            prompt.id, test_user.id, PromptUpdate(content="Modified")
        )

        # Rollback to version 1
        rolled_back = await prompt_service.rollback_to_version(
            prompt.id, test_user.id, version_number=1
        )

        assert rolled_back is not None
        assert rolled_back.content == "Original"

        # Should have 3 versions now (original, modified, rollback)
        versions = await prompt_service.get_versions(prompt.id, test_user.id)
        assert len(versions) == 3
