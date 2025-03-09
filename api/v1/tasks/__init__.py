from fastapi import Depends, APIRouter

from core.dependencies.authentication import AuthenticationRequired

from .tasks import task_router

tasks_router = APIRouter()

tasks_router.include_router(
    task_router,
    tags=["Tasks"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["tasks_router"]