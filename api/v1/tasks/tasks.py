from typing import Callable
from fastapi import APIRouter, Depends, Request

from app.controllers import TaskController
from app.models.tasks import TaskPermission
from app.schemas.requests.tasks import TaskCreate
from app.schemas.responses.tasks import TaskResponse
from core.factory import Factory
from core.dependencies.permissions import Permissions

task_router = APIRouter()

@task_router.get("/", response_model=list[TaskResponse])
async def get_tasks(request: Request, controller: TaskController = Depends(Factory().get_task_controller), assert_permission: Callable = Depends(Permissions(TaskPermission.read))) -> list[TaskResponse]:
    tasks =  await controller.get_by_user_id(request.user.id)
    assert_permission(resource=tasks)
    return tasks

@task_router.post("/", response_model=TaskResponse)
async def create_task(request: Request, task_create: TaskCreate,controller: TaskController = Depends(Factory().get_task_controller)) -> TaskResponse:
    task = await controller.create(title=task_create.title, description=task_create.description, user_id=request.user.id, project_id=task_create.project_id)
    return task

@task_router.get("/{task_uuid}", response_model=TaskResponse)
async def get_task(task_uuid: str, controller: TaskController = Depends(Factory().get_task_controller), assert_permission: Callable = Depends(Permissions(TaskPermission.read))) -> TaskResponse:
    task = await controller.get_by_uuid(task_uuid)
    assert_permission(resource=task)
    return task

@task_router.delete("/{task_uuid}", response_model=TaskResponse)
async def delete_task(task_uuid: str, request: Request, controller: TaskController = Depends(Factory().get_task_controller), assert_permission: Callable = Depends(Permissions(TaskPermission.delete))) -> TaskResponse:
    task = await controller.get_by_uuid(task_uuid)
    assert_permission(resource=task)
    await controller.delete(task)
