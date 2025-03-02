from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, Boolean, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin
from core.security.access_control import Allow, Everyone, RolePrincipal, UserPrincipal, Authenticated


class TaskPermission(Enum):
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'
    

class Task(Base, TimestampMixin):
    __tablename__ = 'tasks'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Unicode(255), unique=True, default=lambda: str(uuid4()), nullable=False)
    title = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    project_id = Column(BigInteger, ForeignKey('projects.id'), nullable=False)
    
    user = relationship('User', back_populates='tasks', uselist=False, lazy="raise")
    
    __mapper_args__ = {'eager_defaults': True}
    def __acl__(self):
        basic_permissions = [TaskPermission.create]
        self_permissions = [
            TaskPermission.read,
            TaskPermission.update,
            TaskPermission.delete
        ]
        all_permissions = list(TaskPermission)
        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.user_id), self_permissions),
            (Allow, RolePrincipal('admin'), all_permissions),
        ]