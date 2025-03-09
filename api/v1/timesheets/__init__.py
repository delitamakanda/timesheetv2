from fastapi import Depends, APIRouter

from core.dependencies.authentication import AuthenticationRequired

from .timesheets import timesheet_router

timesheets_router = APIRouter()

timesheets_router.include_router(
    timesheet_router,
    tags=["Timesheets"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["timesheets_router"]