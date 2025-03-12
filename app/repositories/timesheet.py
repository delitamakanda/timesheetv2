from __future__ import annotations

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Timesheet
from core.repository import BaseRepository

class TimesheetRepository(BaseRepository[Timesheet]):
    """
    Timesheet repository provides all the database operations for the Timesheet model.
    """
    async def get_by_user_id(self, user_id: int, join_: set[str] | None = None) -> list[Timesheet]:
        """
        Get all timesheets for a specific user.

        :param user_id: User ID.
        :param join_: Join relations.
        :return: List of timesheets.
        """
        query = await self._query(join_)
        query = await self._get_by(query, "user_id", user_id)
        if join_ is not None:
            return await self.all_unique(query)
        return await self._all(query)
    
    async def get_by_task_id(self, task_id: int, join_: set[str] | None = None) -> list[Timesheet]:
        """
        Get all timesheets for a specific task.

        :param task_id: Task ID.
        :param join_: Join relations.
        :return: List of timesheets.
        """
        query = await self._query(join_)
        query = await self._get_by(query, "task_id", task_id)
        if join_ is not None:
            return await self.all_unique(query)
        return await self._all(query)
    
    async def get_timesheet_for_period(self, user_id: int, join_: set[str] | None = None) -> list[Timesheet]:
        query = await self._query(join_)
        query = await self._get_by(query, "date")
       