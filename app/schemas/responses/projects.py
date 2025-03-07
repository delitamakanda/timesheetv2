from pydantic import BaseModel, Field

class ProjectResponse(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example='Example Project')
    description: str = Field(..., example='This is an example project.')
    
    class Config:
        from_attributes = True