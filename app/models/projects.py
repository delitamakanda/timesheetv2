from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, Boolean, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin
from core.security.access_control import Allow, Everyone, RolePrincipal, UserPrincipal, Authenticated

class ProjectPermission(Enum):
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'
    


class Project(Base, TimestampMixin):
    __tablename__ = 'projects'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Unicode(255), unique=True, default=lambda: str(uuid4()), nullable=False)
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(255), nullable=False)
    created_by = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    
    __mapper_args__ = { 'eager_defaults': True}
    def __acl__(self):
        basic_permissions = [ProjectPermission.create]
        self_permissions = [
            ProjectPermission.read,
            ProjectPermission.update,
            ProjectPermission.delete
        ]
        all_permissions = list(ProjectPermission)
        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.created_by), self_permissions),
            (Allow, RolePrincipal('admin'), all_permissions),
        ]
    