from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import Timesheet
from core.repository import BaseRepository

class TimesheetRepository(BaseRepository[Timesheet]):
    """
    Timesheet repository provides all the database operations for the Timesheet model.
    """
    pass