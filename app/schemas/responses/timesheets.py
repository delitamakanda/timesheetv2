from pydantic import BaseModel, Field

class TimesheetResponse(BaseModel):
    id: int = Field(..., example=1)
    uuid: str = Field(..., example='123e4567-e89b-12d3-a456-426655440000')
    user_id: int = Field(..., example=1)
    task_id: int = Field(..., example=1)
    date: str = Field(..., example='2022-01-01')
    hours_worked: float = Field(..., example=8.0)
    sap_hours: str = Field(..., example='ABC123')
    
    class Config:
        from_attributes = True