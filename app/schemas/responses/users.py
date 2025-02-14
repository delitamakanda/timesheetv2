from pydantic import UUID4, BaseModel, Field

class UserResponse(BaseModel):
    id: UUID4 = Field(..., example='123e4567-e89b-12d3-a456-426655440000')
    email: str = Field(..., example='john.doe@example.com')
    role: str = Field(..., example='standard')
    
    class Config:
        orm_mode = True
