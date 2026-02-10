"""Prompt management service."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.prompt import PromptTemplate, PromptVersion
from app.schemas.prompt import PromptCreate, PromptUpdate


class PromptService:
    """Service for prompt management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_prompt_by_id(
        self, prompt_id: UUID, user_id: UUID | None = None
    ) -> PromptTemplate | None:
        """Get prompt by ID, optionally filtered by user."""
        query = select(PromptTemplate).where(PromptTemplate.id == prompt_id)
        if user_id:
            query = query.where(PromptTemplate.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_prompt_with_versions(
        self, prompt_id: UUID, user_id: UUID
    ) -> PromptTemplate | None:
        """Get prompt with version history."""
        query = (
            select(PromptTemplate)
            .options(selectinload(PromptTemplate.versions))
            .where(PromptTemplate.id == prompt_id)
            .where(PromptTemplate.user_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_prompts(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20,
        tags: list[str] | None = None,
        favorites_only: bool = False,
    ) -> tuple[list[PromptTemplate], int]:
        """Get paginated list of prompts for a user."""
        query = select(PromptTemplate).where(PromptTemplate.user_id == user_id)
        count_query = select(func.count(PromptTemplate.id)).where(
            PromptTemplate.user_id == user_id
        )

        if favorites_only:
            query = query.where(PromptTemplate.is_favorite == True)
            count_query = count_query.where(PromptTemplate.is_favorite == True)

        if tags:
            # Filter by any of the provided tags
            query = query.where(PromptTemplate.tags.overlap(tags))
            count_query = count_query.where(PromptTemplate.tags.overlap(tags))

        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(PromptTemplate.updated_at.desc())
        result = await self.db.execute(query)
        prompts = list(result.scalars().all())

        return prompts, total

    async def create_prompt(
        self, user_id: UUID, prompt_data: PromptCreate
    ) -> PromptTemplate:
        """Create a new prompt with initial version."""
        prompt = PromptTemplate(
            user_id=user_id,
            name=prompt_data.name,
            description=prompt_data.description,
            content=prompt_data.content,
            tags=prompt_data.tags,
        )
        self.db.add(prompt)
        await self.db.flush()

        # Create initial version
        version = PromptVersion(
            prompt_id=prompt.id,
            version_number=1,
            content=prompt_data.content,
        )
        self.db.add(version)
        await self.db.flush()
        await self.db.refresh(prompt)

        return prompt

    async def update_prompt(
        self, prompt_id: UUID, user_id: UUID, prompt_data: PromptUpdate
    ) -> PromptTemplate | None:
        """Update an existing prompt, creating a new version if content changes."""
        prompt = await self.get_prompt_by_id(prompt_id, user_id)
        if not prompt:
            return None

        update_data = prompt_data.model_dump(exclude_unset=True)
        content_changed = "content" in update_data and update_data["content"] != prompt.content

        # Update fields
        for field, value in update_data.items():
            setattr(prompt, field, value)

        # Create new version if content changed
        if content_changed:
            # Get latest version number
            latest_version = await self._get_latest_version_number(prompt_id)
            new_version = PromptVersion(
                prompt_id=prompt_id,
                version_number=latest_version + 1,
                content=update_data["content"],
            )
            self.db.add(new_version)

        await self.db.flush()
        await self.db.refresh(prompt)
        return prompt

    async def delete_prompt(self, prompt_id: UUID, user_id: UUID) -> bool:
        """Delete a prompt and all its versions."""
        prompt = await self.get_prompt_by_id(prompt_id, user_id)
        if not prompt:
            return False

        await self.db.delete(prompt)
        await self.db.flush()
        return True

    async def toggle_favorite(self, prompt_id: UUID, user_id: UUID) -> PromptTemplate | None:
        """Toggle favorite status of a prompt."""
        prompt = await self.get_prompt_by_id(prompt_id, user_id)
        if not prompt:
            return None

        prompt.is_favorite = not prompt.is_favorite
        await self.db.flush()
        await self.db.refresh(prompt)
        return prompt

    async def get_versions(self, prompt_id: UUID, user_id: UUID) -> list[PromptVersion]:
        """Get all versions of a prompt."""
        # Verify user owns the prompt
        prompt = await self.get_prompt_by_id(prompt_id, user_id)
        if not prompt:
            return []

        query = (
            select(PromptVersion)
            .where(PromptVersion.prompt_id == prompt_id)
            .order_by(PromptVersion.version_number.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def rollback_to_version(
        self, prompt_id: UUID, user_id: UUID, version_number: int
    ) -> PromptTemplate | None:
        """Rollback prompt content to a specific version."""
        prompt = await self.get_prompt_by_id(prompt_id, user_id)
        if not prompt:
            return None

        # Get the target version
        query = select(PromptVersion).where(
            PromptVersion.prompt_id == prompt_id,
            PromptVersion.version_number == version_number,
        )
        result = await self.db.execute(query)
        target_version = result.scalar_one_or_none()

        if not target_version:
            return None

        # Update content (this will create a new version)
        prompt.content = target_version.content

        # Create new version
        latest_version = await self._get_latest_version_number(prompt_id)
        new_version = PromptVersion(
            prompt_id=prompt_id,
            version_number=latest_version + 1,
            content=target_version.content,
        )
        self.db.add(new_version)

        await self.db.flush()
        await self.db.refresh(prompt)
        return prompt

    async def _get_latest_version_number(self, prompt_id: UUID) -> int:
        """Get the latest version number for a prompt."""
        query = select(func.max(PromptVersion.version_number)).where(
            PromptVersion.prompt_id == prompt_id
        )
        result = await self.db.execute(query)
        latest = result.scalar()
        return latest or 0
