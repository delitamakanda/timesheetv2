from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, Unicode, Integer, ForeignKey, Float, Date, String

from core.database import Base
from core.database.mixins import TimestampMixin
from core.security.access_control import Allow, RolePrincipal, UserPrincipal, Authenticated

class TimesheetPermission(Enum):
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'
    
class Timesheet(Base, TimestampMixin):
    __tablename__ = 'timesheets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(Unicode(255), unique=True, default=lambda: str(uuid4()), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    date = Column(Date, nullable=False)
    hours_worked = Column(Float, nullable=False)
    sap_hours = Column(String, nullable=False)
    
    __mapper_args__ =  {'eager_defaults': True}
    def __acl__(self):
        basic_permissions = [TimesheetPermission.create]
        self_permissions = [
            TimesheetPermission.read,
            TimesheetPermission.update,
            TimesheetPermission.delete
        ]
        all_permissions = list(TimesheetPermission)
        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(value=self.user_id), self_permissions),
            (Allow, RolePrincipal(value='admin'), all_permissions),
        ]
    