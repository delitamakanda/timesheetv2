from fastapi import Depends, Request
from app.controllers.user import UserController
from core.factory import Factory


async def get_current_user(
        request: Request,
        controller: UserController = Depends(Factory().get_user_controller),
):
    return await controller.get_by_id(request.user.id)
