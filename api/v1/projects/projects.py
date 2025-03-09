from typing import Callable
from fastapi import APIRouter, Depends, Request
from app.controllers import ProjectController
from app.models.projects import ProjectPermission
from app.schemas.requests.projects import ProjectCreate
from app.schemas.responses.projects import ProjectResponse
from core.factory import Factory
from core.dependencies.permissions import Permissions

project_router = APIRouter()

@project_router.get("/", response_model=list[ProjectResponse])
async def get_projects(request: Request, controller: ProjectController = Depends(Factory().get_project_controller), assert_permission: Callable = Depends(Permissions(ProjectPermission.read))) -> list[ProjectResponse]:
    projects = await controller.get_by_user_id(request.user.id)
    assert_permission(resource=projects)
    return projects

@project_router.post("/", response_model=ProjectResponse)
async def create_project(request: Request, project_create: ProjectCreate, controller: ProjectController = Depends(Factory().get_project_controller)) -> ProjectResponse:
    project = await controller.create(name=project_create.name, description=project_create.description, created_by=request.user.id)
    return project

@project_router.get("/{project_uuid}", response_model=ProjectResponse)
async def get_project(project_uuid: str, controller: ProjectController = Depends(Factory().get_project_controller), assert_permission: Callable = Depends(Permissions(ProjectPermission.read))) -> ProjectResponse:
    project = await controller.get_by_uuid(project_uuid)
    assert_permission(resource=project)
    return project

