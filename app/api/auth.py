from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    # Supabase: send magic link
    res = supabase.auth.sign_in_with_otp({"email": data.email})
    if res.get("error"):
        raise HTTPException(status_code=400, detail=res["error"]["message"])
    return MagicLinkResponse(message="Magic link sent to email.")

@router.post("/set-password", response_model=MagicLinkResponse)
def set_password(data: SetPasswordRequest) -> MagicLinkResponse:
    # Supabase: update password using token
    res = supabase.auth.verify_otp({"token": data.token, "type": "email"})
    if res.get("error"):
        raise HTTPException(status_code=400, detail=res["error"]["message"])
    user = res.get("user")
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token.")
    # Now update password
    update_res = supabase.auth.update_user({"password": data.password})
    if update_res.get("error"):
        raise HTTPException(status_code=400, detail=update_res["error"]["message"])
    return MagicLinkResponse(message="Password set successfully.")

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest) -> LoginResponse:
    res = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    if res.get("error"):
        raise HTTPException(status_code=401, detail=res["error"]["message"])
    session = res.get("session")
    user = res.get("user")
    if not session or not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return LoginResponse(
        access_token=session["access_token"],
        token_type="bearer",
        user=user
    )

@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(data: ResetPasswordRequest) -> ResetPasswordResponse:
    res = supabase.auth.reset_password_for_email(data.email)
    if res.get("error"):
        raise HTTPException(status_code=400, detail=res["error"]["message"])
    return ResetPasswordResponse(message="Password reset email sent.")

@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest) -> RegisterResponse:
    # You can adapt this to use supabase.auth.sign_up if you want
    return RegisterResponse(
        id="2",
        email=data.email,
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name
    )

def get_current_user(authorization: str = Header(...)):
    # Extract and validate the Bearer token using Supabase
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    res = supabase.auth.get_user(token)
    if not res.get("user"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return res["user"]

@router.get("/me")
def me(user=Depends(get_current_user)) -> UserResponse:
    # Return the authenticated user's info from Supabase
    return UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["user_metadata"].get("username", ""),
        first_name=user["user_metadata"].get("first_name", ""),
        last_name=user["user_metadata"].get("last_name", ""),
        birth_date=user["user_metadata"].get("birth_date", ""),
        document_id=user["user_metadata"].get("document_id", ""),
        address=user["user_metadata"].get("address", ""),
        phone=user["user_metadata"].get("phone", "")
    ) 