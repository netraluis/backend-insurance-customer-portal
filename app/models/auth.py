from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

class MagicLinkRequest(BaseModel):
    email: EmailStr

class MagicLinkResponse(BaseModel):
    message: str

class SetPasswordRequest(BaseModel):
    token: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordResponse(BaseModel):
    message: str

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    birth_date: str
    document_id: str  # NRT/NIA/Passport
    email: EmailStr
    address: str
    user_id: str
    username: str
    phone: str
    password: str

class RegisterResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    birth_date: str
    document_id: str
    address: str
    phone: str 