from datetime import datetime, timedelta
from dateutils import relativedelta
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


@timesheet_router.get("/month/current", response_model=TimesheetResponse)
async def get_current_month_timesheet(request: Request, controller: TimesheetController = Depends(Factory().get_timesheet_controller), assert_permission: Callable = Depends(Permissions(TimesheetPermission.read))):
    now = datetime.now()
    start_of_month = now.replace(day=1)
    end_of_month = start_of_month + relativedelta(month=1) - timedelta(days=1)
    timesheet = await controller.get_timesheet_for_period(
        user_id=request.user.id,
        start_date=start_of_month,
        end_date=end_of_month
    )
    assert_permission(resource=timesheet)
    return timesheet


@timesheet_router.get("/month/previous", response_model=TimesheetResponse)
def get_previous_month_timesheet(request: Request, controller: TimesheetController = Depends(Factory().get_timesheet_controller), assert_permission: Callable = Depends(Permissions(TimesheetPermission.read))):
    pass


@timesheet_router.get("/year/current", response_model=TimesheetResponse)
def get_current_year_timesheet(request: Request, controller: TimesheetController = Depends(Factory().get_timesheet_controller), assert_permission: Callable = Depends(Permissions(TimesheetPermission.read))):
    pass


@timesheet_router.get("/year/{year}", response_model=TimesheetResponse)
def get_year_timesheet(request: Request, controller: TimesheetController = Depends(Factory().get_timesheet_controller), assert_permission: Callable = Depends(Permissions(TimesheetPermission.read))):
    pass
