from pydantic import BaseModel, Field

class TaskResponse(BaseModel):
    id: int = Field(..., example=1)
    uuid: str = Field(..., example='123e4567-e89b-12d3-a456-426655440000')
    title: str = Field(..., example='Example Task')
    description: str = Field(..., example='This is an example tasks.')
    project_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    
    class Config:
        from_attributes = True