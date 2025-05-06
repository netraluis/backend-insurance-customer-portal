from fastapi import APIRouter, Depends, Header
from app.models.auth import (
    MagicLinkRequest, MagicLinkResponse, SetPasswordRequest, LoginRequest, LoginResponse,
    ResetPasswordRequest, ResetPasswordResponse, RegisterRequest, RegisterResponse, UserResponse,
    ValidationEmailRequest, ValidationEmailResponse, VerifyOTPRequest, VerifyOTPResponse
)
from app.models.base import APIResponse, APIError, api_response
import os
from supabase import create_client, Client
from app.services.auth_service import (
    send_magic_link_service,
    set_password_service,
    login_service,
    reset_password_service,
    register_service,
    get_current_user_service,
    send_otp_email_service,
    verify_otp_service
)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

# --- Endpoints ---

@router.post("/validation-email", response_model=APIResponse[ValidationEmailResponse])
def send_validation_email(data: ValidationEmailRequest):
    return send_otp_email_service(data)

@router.post("/magic-link", response_model=APIResponse[MagicLinkResponse])
def send_magic_link(data: MagicLinkRequest):
    return send_magic_link_service(data)

@router.post("/set-password", response_model=APIResponse[MagicLinkResponse])
def set_password(data: SetPasswordRequest):
    return set_password_service(data)

@router.post("/login", response_model=APIResponse[LoginResponse])
def login(data: LoginRequest):
    return login_service(data)

@router.post("/reset-password", response_model=APIResponse[ResetPasswordResponse])
def reset_password(data: ResetPasswordRequest):
    return reset_password_service(data)

@router.post("/register", response_model=APIResponse[RegisterResponse])
def register(data: RegisterRequest):
    return register_service(data)

@router.post("/verify-otp", response_model=APIResponse[VerifyOTPResponse])
def verify_otp(data: VerifyOTPRequest):
    return verify_otp_service(data)

def get_current_user(authorization: str = Header(...)):
    return get_current_user_service(authorization)

@router.get("/me", response_model=APIResponse[UserResponse])
def me(user=Depends(get_current_user)):
    # Return the authenticated user's info from Supabase
    return api_response(
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
        status_code=200
    ) 