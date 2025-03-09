from __future__ import annotations

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Task
from core.repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    """
    Task repository provides all the database operations for the Task model.
    """
    async def get_by_user_id(
            self, user_id: int, join_: set[str] | None = None
    ) -> list[Task]:
        """
        Get all tasks for a specific user.

        :param user_id: User ID.
        :param join_: Join relations.
        :return: List of tasks.
        """
        query = await self._query(join_)
        query = await self._get_by(query, "user_id", user_id)
        if join_ is not None:
            return await self.all_unique(query)
        return await self._all(query)
    
    async def get_by_project_id(
            self, project_id: int, join_: set[str] | None = None
    ) -> list[Task]:
        """
        Get all tasks for a specific project.

        :param project_id: Project ID.
        :param join_: Join relations.
        :return: List of tasks.
        """
        query = await self._query(join_)
        query = await self._get_by(query, "project_id", project_id)
        if join_ is not None:
            return await self.all_unique(query)
        return await self._all(query)
    
    def _join_user(self, query: Select) -> Select:
        """
        Join user.

        :param query: SQLAlchemy query.
        :return: SQLAlchemy query with joined user.
        """
        return query.options(joinedload(Task.user))
    
    