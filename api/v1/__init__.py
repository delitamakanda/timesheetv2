from fastapi import APIRouter
from .monitoring import monitoring_router
from .users import users_router
from .tasks import tasks_router
from .projects import projects_router
from .timesheets import timesheets_router

v1_router = APIRouter()
v1_router.include_router(monitoring_router, prefix="/monitoring")
v1_router.include_router(users_router, prefix="/users")
v1_router.include_router(tasks_router, prefix="/tasks")
v1_router.include_router(projects_router, prefix="/projects")
v1_router.include_router(timesheets_router, prefix="/timesheets")
