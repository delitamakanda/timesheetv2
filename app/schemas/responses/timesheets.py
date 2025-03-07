from pydantic import BaseModel, Field

class TimesheetResponse(BaseModel):
    id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    task_id: int = Field(..., example=1)
    date: str = Field(..., example='2022-01-01')
    hours: float = Field(..., example=8.0)
    sap_code: str = Field(..., example='ABC123')
    
    class Config:
        from_attributes = True