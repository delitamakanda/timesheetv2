from pydantic import EmailStr
from app.models import User
from app.repositories import UserRepository
from app.schemas.extras.token import Token
from core.controller import BaseController
from core.database import Propagation, Transactional
from core.exceptions import BadRequestException, UnauthorizedException
from core.security import JWTManager, PasswordManager


class AuthController(BaseController[User]):
    def __init__(self, user_repo: UserRepository):
        super().__init__(User, user_repo)
        self.user_repo = user_repo
    
    @Transactional(propagation=Propagation.REQUIRED)
    async def register(self, username: str, email: EmailStr, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if user:
            raise BadRequestException("Email already registered")
        
        user = await self.user_repo.get_by_username(username)
        if user:
            raise BadRequestException("Username already taken")
        
        password = PasswordManager.hash_password(password)
        return {
            "email": email,
            "username": username,
            "password": password,
        }
    
    async def login(self, email: EmailStr, password: str) -> Token:
        user = await  self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedException("Invalid email or password")
        if not PasswordManager.verify_password(password, user.password):
            raise UnauthorizedException("Invalid email or password")
        return Token(
            access_token=JWTManager.encode(payload={"user_id": user.id}),
            refresh_token=JWTManager.encode(payload={"sub": "refresh_token"})
        )
    
    @staticmethod
    async def refresh_token(access_token: str, refresh_token: str) -> Token:
        token = JWTManager.decode(access_token)
        refresh_token = JWTManager.decode(refresh_token)
        if refresh_token["sub"] != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")
        return Token(
            access_token=JWTManager.encode(payload={"user_id": token["user_id"]}),
            refresh_token=JWTManager.encode(payload={"sub": "refresh_token"})
        )