from sqlalchemy import Select
from sqlalchemy.orm import joinedload
from app.models import Project
from core.repository import BaseRepository



class ProjectRepository(BaseRepository[Project]):
    """
    Project repository provides all the database operations for the Project model.
    """
    pass
    