from pydantic import BaseModel, Field

class ProjectResponse(BaseModel):
    id: int = Field(..., example=1)
    uuid: str = Field(..., example='123e4567-e89b-12d3-a456-426655440000')
    name: str = Field(..., example='Example Project')
    description: str = Field(..., example='This is an example project.')
    
    class Config:
        from_attributes = True