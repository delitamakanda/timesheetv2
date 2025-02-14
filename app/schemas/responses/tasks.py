from pydantic import BaseModel, Field

class TaskResponse(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example='Example Task')
    description: str = Field(..., example='This is an example task.')
    project_id: int = Field(..., example=1)
    assigned_to: int = Field(..., example=1)
    
    class Config:
        orm_mode = True