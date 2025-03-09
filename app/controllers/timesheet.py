from datetime import datetime

from app.models import Timesheet
from app.repositories import TimesheetRepository
from core.controller import BaseController
from core.database import Propagation, Transactional


class TimesheetController(BaseController[Timesheet]):
    def __init__(self, timesheet_repo: TimesheetRepository):
        super().__init__(model=Timesheet, repository=timesheet_repo)
        self.timesheet_repo = timesheet_repo
        
    
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, user_id: int, task_id: int, date: str, hours_worked: float, sap_hours: str) -> Timesheet:
        return await self.repository.create({
            'user_id': user_id,
            'task_id': task_id,
            'date': datetime.strptime(date, '%Y-%m-%d'),
            'hours_worked': hours_worked,
            'sap_hours': sap_hours
        })
    
    
    async def get_by_user_id(self, user_id: int) -> list[Timesheet]:
        return await self.timesheet_repo.get_by_user_id(user_id)
    
    async def get_by_task_id(self, task_id: int) -> list[Timesheet]:
        return await self.timesheet_repo.get_by_task_id(task_id)