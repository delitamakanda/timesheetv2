from pydantic import BaseModel


class TimesheetCreate(BaseModel):
    task_id: int
    date: date
    hours: float