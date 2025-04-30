from fastapi import APIRouter, HTTPException, Depends, Header
from app.models.auth import (
    MagicLinkRequest, MagicLinkResponse, SetPasswordRequest, LoginRequest, LoginResponse,
    ResetPasswordRequest, ResetPasswordResponse, RegisterRequest, RegisterResponse, UserResponse
)
from app.models.base import APIResponse, APIError
import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

# --- Endpoints ---

@router.post("/magic-link", response_model=APIResponse[MagicLinkResponse])
def send_magic_link(data: MagicLinkRequest):
    res = supabase.auth.sign_in_with_otp({"email": data.email})
    if res.get("error"):
        return APIResponse(data=None, error=APIError(message=res["error"]["message"]), count=None, status_code=400)
    return APIResponse(data=MagicLinkResponse(message="Magic link sent to email."), error=None, count=None, status_code=200)

@router.post("/set-password", response_model=APIResponse[MagicLinkResponse])
def set_password(data: SetPasswordRequest):
    res = supabase.auth.verify_otp({"token": data.token, "type": "email"})
    if res.get("error"):
        return APIResponse(data=None, error=APIError(message=res["error"]["message"]), count=None, status_code=400)
    user = res.get("user")
    if not user:
        return APIResponse(data=None, error=APIError(message="Invalid token."), count=None, status_code=400)
    update_res = supabase.auth.update_user({"password": data.password})
    if update_res.get("error"):
        return APIResponse(data=None, error=APIError(message=update_res["error"]["message"]), count=None, status_code=400)
    return APIResponse(data=MagicLinkResponse(message="Password set successfully."), error=None, count=None, status_code=200)

@router.post("/login", response_model=APIResponse[LoginResponse])
def login(data: LoginRequest):
    res = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    if res.get("error"):
        return APIResponse(data=None, error=APIError(message=res["error"]["message"]), count=None, status_code=401)
    session = res.get("session")
    user = res.get("user")
    if not session or not user:
        return APIResponse(data=None, error=APIError(message="Invalid credentials."), count=None, status_code=401)
    return APIResponse(
        data=LoginResponse(
            access_token=session["access_token"],
            token_type="bearer",
            user=user
        ),
        error=None,
        count=None,
        status_code=200
    )

@router.post("/reset-password", response_model=APIResponse[ResetPasswordResponse])
def reset_password(data: ResetPasswordRequest):
    res = supabase.auth.reset_password_for_email(data.email)
    if res.get("error"):
        return APIResponse(data=None, error=APIError(message=res["error"]["message"]), count=None, status_code=400)
    return APIResponse(data=ResetPasswordResponse(message="Password reset email sent."), error=None, count=None, status_code=200)

@router.post("/register", response_model=APIResponse[RegisterResponse])
def register(data: RegisterRequest):
    # You can adapt this to use supabase.auth.sign_up if you want
    return APIResponse(
        data=RegisterResponse(
            id="2",
            email=data.email,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name
        ),
        error=None,
        count=None,
        status_code=201
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

@router.get("/me", response_model=APIResponse[UserResponse])
def me(user=Depends(get_current_user)):
    # Return the authenticated user's info from Supabase
    return APIResponse(
        data=UserResponse(
            id=user["id"],
            email=user["email"],
            username=user["user_metadata"].get("username", ""),
            first_name=user["user_metadata"].get("first_name", ""),
            last_name=user["user_metadata"].get("last_name", ""),
            birth_date=user["user_metadata"].get("birth_date", ""),
            document_id=user["user_metadata"].get("document_id", ""),
            address=user["user_metadata"].get("address", ""),
            phone=user["user_metadata"].get("phone", "")
        ),
        error=None,
        count=None,
        status_code=200
    ) 