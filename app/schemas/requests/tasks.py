from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str
    description: str
    project_id: int
    assigned_to: int