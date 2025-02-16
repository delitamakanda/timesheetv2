from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.exceptions.base import CustomException

class BearerAuthError(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    message = "Authentication required"
    error_code = status.HTTP_401_UNAUTHORIZED
    
class AuthenticationRequired:
    def __init__(self, token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
        if not token:
            raise BearerAuthError()