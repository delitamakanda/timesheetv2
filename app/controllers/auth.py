from pydantic import EmailStr
from app.models import User
from app.repositories import UserRepository
from app.schemas.extras.token import Token
from core.controller import BaseController
from core.database import Propagation, Transactional
from core.exceptions import BadRequestException, UnauthorizedException
from core.security import JWTHandler, PasswordHandler


class AuthController(BaseController[User]):
    def __init__(self, user_repo: UserRepository):
        super().__init__(model=User, repository=user_repo)
        self.user_repo = user_repo
    
    @Transactional(propagation=Propagation.REQUIRED)
    async def register(self, username: str, email: EmailStr, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if user:
            raise BadRequestException("Email already registered")
        
        user = await self.user_repo.get_by_username(username)
        if user:
            raise BadRequestException("Username already taken")
        
        password = PasswordHandler.hash(password)
        return await self.user_repo.create({
            "email": str(email),
            "username": username,
            "password_hash": password,
        })
    
    async def login(self, email: EmailStr, password: str) -> Token:
        user = await  self.user_repo.get_by_email(email)
        if not user:
            raise BadRequestException("Invalid email or password")
        if not PasswordHandler.verify(user.password_hash, password):
            raise BadRequestException("Invalid email or password")
        return Token(
            access_token=JWTHandler.encode(payload={"user_id": user.id}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"})
        )
    
    async def refresh_token(self, access_token: str, refresh_token: str) -> Token:
        token = JWTHandler.decode(access_token)
        refresh_token = JWTHandler.decode(refresh_token)
        if refresh_token.get('sub') != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")
        return Token(
            access_token=JWTHandler.encode(payload={"user_id": token.get('user_id')}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"})
        )