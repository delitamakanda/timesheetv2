from typing import Callable, Any, Coroutine
from fastapi import APIRouter, Depends

from app.controllers import AuthController, UserController
from app.models.users import User, UserPermission
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginRequest, RegisterRequest
from core.factory import Factory
from core.dependencies import AuthenticationRequired
from core.dependencies.current_user import get_current_user
from app.schemas.responses.users import UserResponse
from core.dependencies.permissions import Permissions


user_router = APIRouter()

@user_router.get("/", dependencies=[Depends(AuthenticationRequired)])
async def get_all_users(controller: UserController = Depends(Factory().get_user_controller),
                        assert_permission: Callable = Depends(Permissions(UserPermission.read))) -> list[UserResponse]:
    users = await controller.get_all()
    assert_permission(resource=users)
    return users

@user_router.post("/login")
async def login(request: LoginRequest,
                controller: AuthController = Depends(Factory().get_auth_controller),) -> Token:
     return await controller.login(email = request.email, password= request.password_hash)


@user_router.post("/register", status_code=201)
async def register(request: RegisterRequest,
                   controller: AuthController = Depends(Factory().get_auth_controller)) -> UserResponse:
     return await controller.register(username=request.username, email=request.email, password=request.password_hash)

@user_router.get("/me", response_model=UserResponse, dependencies=[Depends(AuthenticationRequired)])
async def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    return user
