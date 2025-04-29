from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

# --- Input/Output Models ---

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
    user: dict

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

# --- Endpoints ---

@router.post("/magic-link", response_model=MagicLinkResponse)
def send_magic_link(data: MagicLinkRequest) -> MagicLinkResponse:
    """Send a magic link to the user's email for account activation or password setup (mocked)."""
    return MagicLinkResponse(message="Magic link sent to email.")

@router.post("/set-password", response_model=MagicLinkResponse)
def set_password(data: SetPasswordRequest) -> MagicLinkResponse:
    """Set a new password using a token from the magic link (mocked)."""
    return MagicLinkResponse(message="Password set successfully.")

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest) -> LoginResponse:
    """Authenticate user and return JWT token and user info (mocked)."""
    return LoginResponse(
        access_token="mocked.jwt.token",
        token_type="bearer",
        user={
            "id": "1",
            "email": data.email,
            "username": "johnsmith",
            "first_name": "John",
            "last_name": "Smith"
        }
    )

@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(data: ResetPasswordRequest) -> ResetPasswordResponse:
    """Send a password reset email to the user (mocked)."""
    return ResetPasswordResponse(message="Password reset email sent.")

@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest) -> RegisterResponse:
    """Register a new user (mocked)."""
    return RegisterResponse(
        id="2",
        email=data.email,
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name
    )

@router.get("/me", response_model=UserResponse)
def me() -> UserResponse:
    """Get the authenticated user's info (mocked)."""
    return UserResponse(
        id="1",
        email="test@example.com",
        username="johnsmith",
        first_name="John",
        last_name="Smith",
        birth_date="1990-01-01",
        document_id="NRT123456",
        address="123 Main St, Anytown, USA",
        phone="+123456789"
    ) 