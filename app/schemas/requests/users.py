from pydantic import BaseModel, EmailStr, constr
import re

from pydantic.v1 import validator


class UserCreate(BaseModel):
    email: str
    password_hash: str
    username: constr(min_length=3, max_length=30)


class LoginRequest(BaseModel):
    email: EmailStr
    password_hash: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password_hash: constr(min_length=8, max_length=128)
    username: constr(min_length=3, max_length=30)
    
    @validator('password_hash')
    def password_must_contain_special_characters(cls, v):
        if not re.search(r'[^a-zA-Z0-9]', v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    @validator('password_hash')
    def password_must_contain_uppercase(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v
    
    @validator('password_hash')
    def password_must_contain_numbers(cls, v):
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('password_hash')
    def password_must_contain_lowercase(cls, v):
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v
    
    @validator('username')
    def username_must_not_contain_special_characters(cls, v):
        if re.search(r'[^a-zA-Z0-9_]', v):
            raise ValueError('Username must not contain special characters')
        return v
