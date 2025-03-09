from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str
    created_by: int