from typing import List

from pydantic import AnyHttpUrl
from enum import Enum

from pydantic.v1 import BaseSettings


class EnvironmentType(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"
    
class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    DATABASE_URL: str = "sqlite:///./timesheet.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300
    DEBUG: bool = True
    ENVIRONMENT: EnvironmentType = EnvironmentType.development
    DEFAULT_LOCALE: str = "fr_FR"
    SHOW_SQL_ALCHEMY_QUERIES: bool = False
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_EMAIL_DOMAINS: List[str] = ["example.com"]
    ALLOWED_ROLES: List[str] = ["standard", "admin", "manager"]
    
    class Config:
        case_sensitive = True


config: Config = Config()