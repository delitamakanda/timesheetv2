from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, Boolean, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from core.database.mixins import TimestampMixin
from core.security.access_control import Allow, Everyone, RolePrincipal, UserPrincipal


class UserPermission(Enum):
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'



class User(Base, TimestampMixin):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Unicode(255), unique=True, default=lambda: str(uuid4()), nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    password_hash = Column(Unicode(255), nullable=False)
    username = Column(Unicode(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    tasks = relationship('Task', back_populates='user', lazy="raise")
    
    __mapper_args__ = {'eager_defaults': True}
    
    @staticmethod
    def __acl__(self):
        basic_permissions = [UserPermission.read, UserPermission.create]
        self_permissions = [
            UserPermission.read,
            UserPermission.update,
            UserPermission.create
        ]
        all_permissions = list(UserPermission)
        return [
            (Allow, Everyone, basic_permissions),
            (Allow, UserPrincipal(self.id), self_permissions),
            (Allow, RolePrincipal('admin'), all_permissions),
        ]
