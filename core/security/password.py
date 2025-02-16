from passlib.context import CryptContext

class PasswordManager:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    @staticmethod
    def hash_password(password: str) -> str:
        return PasswordManager.pwd_context.hash(password)
    
    @staticmethod
    def verify_password(hashed_password: str, password: str) -> bool:
        return PasswordManager.pwd_context.verify(password, hashed_password)