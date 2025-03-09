from functools import partial
from fastapi import Depends

from app.controllers import AuthController, UserController, TaskController, ProjectController, TimesheetController
from app.models import User, Task, Project, Timesheet
from app.repositories import UserRepository, TaskRepository, ProjectRepository, TimesheetRepository
from core.database import get_session

class Factory:
    """
    Factory for creating controllers and repositories.
    """
    user_repo = partial(UserRepository, User)
    task_repo = partial(TaskRepository, Task)
    project_repo = partial(ProjectRepository, Project)
    timesheet_repo = partial(TimesheetRepository, Timesheet)
    
    def get_user_controller(self, db_session = Depends(get_session)):
        return UserController(user_repo=self.user_repo(db_session=db_session))
    
    def get_auth_controller(self, db_session = Depends(get_session)):
        return AuthController(user_repo=self.user_repo(db_session=db_session))
    
    def get_task_controller(self, db_session = Depends(get_session)):
        return TaskController(task_repo=self.task_repo(db_session=db_session))
    
    def get_project_controller(self, db_session = Depends(get_session)):
        return ProjectController(project_repo=self.project_repo(db_session=db_session))
    
    def get_timesheet_controller(self, db_session = Depends(get_session)):
        return TimesheetController(timesheet_repo=self.timesheet_repo(db_session=db_session))