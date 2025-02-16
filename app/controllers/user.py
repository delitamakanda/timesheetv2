from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController


class UserController(BaseController[User]):
    def __init__(self, user_repo: UserRepository):
        super().__init__(User, user_repo)
        self.user_repo = user_repo
        
    async def get_by_username(self, username: str) -> User:
        return await self.user_repo.get_by_username(username)
    
    async def get_by_email(self, email: str) -> User:
        return await self.user_repo.get_by_email(email)
    