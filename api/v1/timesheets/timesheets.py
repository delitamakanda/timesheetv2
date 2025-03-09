from typing import Callable
from fastapi import APIRouter, Depends, Request

from app.controllers import TimesheetController
from app.models.timesheets import TimesheetPermission
from app.schemas.requests.timesheets import TimesheetCreate
from app.schemas.responses.timesheets import TimesheetResponse
from core.factory import Factory
from core.dependencies.permissions import Permissions

timesheet_router = APIRouter()

@timesheet_router.post("/", response_model=TimesheetResponse)
async def create_timesheet(request: Request, timesheet_create: TimesheetCreate,
                          controller: TimesheetController = Depends(Factory().get_timesheet_controller),
                          assert_permission: Callable = Depends(Permissions(TimesheetPermission.create))) -> TimesheetResponse:
    timesheet = await controller.create(
        task_id=timesheet_create.task_id,
        date=timesheet_create.date,
        sap_hours=timesheet_create.sap_hours,
        user_id=request.user.id,
        hours_worked=timesheet_create.hours_worked,

    )
    assert_permission(resource=timesheet_create)
    return timesheet


@timesheet_router.get("/", response_model=list[TimesheetResponse])
async def get_timesheets_by_user_id(request: Request,
                                   controller: TimesheetController = Depends(Factory().get_timesheet_controller),
                                   assert_permission: Callable = Depends(Permissions(TimesheetPermission.read))):
    timesheets = await controller.get_by_user_id(request.user.id)
    assert_permission(resource=timesheets)
    return timesheets


@timesheet_router.get("/{task_id}", response_model=list[TimesheetResponse])
async def get_timesheets_by_task_id(task_id: str,
                                   controller: TimesheetController = Depends(Factory().get_timesheet_controller),
                                   assert_permission: Callable = Depends(Permissions(TimesheetPermission.read))):
    timesheets = await controller.get_by_task_id(task_id)
    assert_permission(resource=timesheets)
    return timesheets

@timesheet_router.delete("/{timesheet_uuid}", response_model=TimesheetResponse)
async def delete_timesheet(timesheet_uuid: str, request: Request,
                          controller: TimesheetController = Depends(Factory().get_timesheet_controller),
                          assert_permission: Callable = Depends(Permissions(TimesheetPermission.delete))):
    timesheet = await controller.get_by_uuid(timesheet_uuid)
    assert_permission(resource=timesheet)
    await controller.delete(timesheet)
    
