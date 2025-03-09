from pydantic import BaseModel


class TimesheetCreate(BaseModel):
    task_id: int
    date: str
    sap_hours: str
    user_id: int
    hours_worked: float