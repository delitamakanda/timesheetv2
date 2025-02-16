from datetime import datetime, timedelta

from jose import  ExpiredSignatureError, JWTError, jwt

from core.config import config
from core.exceptions import CustomException

class JWTDecodeError(CustomException):
    code = 401
    message = "Invalid JWT token"
    

class JWTExpiredError(CustomException):
    code = 401
    message = "JWT token expired"
    
class JWTManager:
    secret_key = config.JWT_SECRET_KEY
    algorithm = config.JWT_ALGORITHM
    expire_minutes = config.JWT_EXPIRE_MINUTES
    
    @staticmethod
    def encode(payload: dict) -> str:
        expire = datetime.now() + timedelta(minutes=JWTManager.expire_minutes)
        payload.update({"exp": expire})
        return jwt.encode(payload, JWTManager.secret_key, algorithm=JWTManager.algorithm)
    
    @staticmethod
    def decode(token: str) -> dict:
        try:
            payload = jwt.decode(token, JWTManager.secret_key, algorithms=[JWTManager.algorithm])
            return payload
        except ExpiredSignatureError as exception:
            raise JWTExpiredError() from exception
        except JWTError as exception:
            raise JWTDecodeError() from exception
    
    @staticmethod
    def decode_expired(token: str) -> dict:
        try:
            return jwt.decode(token, JWTManager.secret_key, algorithms=[JWTManager.algorithm], options={"verify_exp": False})
        except ExpiredSignatureError as exception:
            raise JWTDecodeError() from exception