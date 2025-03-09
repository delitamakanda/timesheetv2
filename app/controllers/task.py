from app.models import Task
from app.repositories import TaskRepository
from core.controller import BaseController
from core.database import Propagation, Transactional

class TaskController(BaseController[Task]):
    def __init__(self, task_repo: TaskRepository):
        super().__init__(model=Task, repository=task_repo)
        self.task_repo = task_repo
        
    async def get_by_project_id(self, project_id: int) -> list[Task]:
        return await self.task_repo.get_by_project_id(project_id)
    
    async def get_by_user_id(self, user_id: int) -> list[Task]:
        return await self.task_repo.get_by_user_id(user_id)
    
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, title: str, description: str, user_id: int, project_id: int) -> Task:
        return await self.repository.create({
            'title': title,
            'description': description,
            'user_id': user_id,
            'project_id': project_id
        })
