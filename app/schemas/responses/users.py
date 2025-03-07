from pydantic import UUID4, BaseModel, Field

class UserResponse(BaseModel):
    email: str = Field(..., example='john.doe@example.com')
    username: str = Field(..., example='john_doe')
    uuid: UUID4 = Field(..., example='123e4567-e89b-12d3-a456-42665544')
    
    
    class Config:
        from_attributes = True
