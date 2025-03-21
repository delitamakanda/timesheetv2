from __future__ import annotations

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import User
from core.repository import BaseRepository
from pydantic import EmailStr


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """
    
    async def get_by_username(
            self, username: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by username.

        :param username: Username.
        :param join_: Join relations.
        :return: User.
        """
        query = await self._query(join_)
        query = query.filter(User.username == username)
        
        if join_ is not None:
            return await self.all_unique(query)
        
        return await self._one_or_none(query)
    
    async def get_by_email(
            self, email: EmailStr, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        query = await self._query(join_)
        query = query.filter(User.email == str(email))
        
        if join_ is not None:
            return await self.all_unique(query)
        
        return await self._one_or_none(query)
    
    def _join_tasks(self, query: Select) -> Select:
        """
        Join tasks.

        :param query: Query.
        :return: Query.
        """
        return query.options(joinedload(User.tasks)).execution_options(
            contains_joined_collection=True
        )