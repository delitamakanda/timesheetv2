from app.models import Project
from app.repositories import ProjectRepository
from core.controller import BaseController
from core.database import Propagation, Transactional

class ProjectController(BaseController[Project]):
    def __init__(self, project_repo: ProjectRepository):
        super().__init__(model=Project, repository=project_repo)
        self.project_repo = project_repo
        
    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, name: str, description: str, created_by: int) -> Project:
        return await self.repository.create({
            'name': name,
            'description': description,
            'created_by': created_by
        })
    
    async def get_by_user_id(self, created_by: int) -> list[Project]:
        return await self.project_repo.get_by_user_id(created_by)
    