from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, Boolean, Unicode, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from core.database.mixins import TimestampMixin

class UserPermission(Enum):
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'
    
class UserRole(Enum):
    admin = 'admin'
    standard = 'standard'
    manager = 'manager'
    
class User(Base, TimestampMixin):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Unicode(36), unique=True, default=lambda: str(uuid4()))
    email = Column(Unicode(255), unique=True, nullable=False)
    password_hash = Column(Unicode(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    
    __mapper_args__ = {'eager_defaults': True }
    
    @staticmethod
    def __acl__():
        basic_permissions = [UserPermission.read, UserPermission.create]
        self_permissions = [
            UserPermission.read,
            UserPermission.update,
            UserPermission.create
        ]
        all_permissions = list(UserPermission)
        return []
        