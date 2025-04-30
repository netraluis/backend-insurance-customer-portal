import os
from supabase import create_client, Client
from app.models.auth import (
    MagicLinkRequest, MagicLinkResponse, SetPasswordRequest, LoginRequest, LoginResponse,
    ResetPasswordRequest, ResetPasswordResponse, RegisterRequest, RegisterResponse, UserResponse
)
from app.models.base import APIResponse, APIError, api_response

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_magic_link_service(data: MagicLinkRequest):
    res = supabase.auth.sign_in_with_otp({"email": data.email})
    if res.get("error"):
        return api_response(error=APIError(message=res["error"]["message"]), status_code=400)
    return api_response(data=MagicLinkResponse(message="Magic link sent to email."), status_code=200)

def set_password_service(data: SetPasswordRequest):
    res = supabase.auth.verify_otp({"token": data.token, "type": "email"})
    if res.get("error"):
        return api_response(error=APIError(message=res["error"]["message"]), status_code=400)
    user = res.get("user")
    if not user:
        return api_response(error=APIError(message="Invalid token."), status_code=400)
    update_res = supabase.auth.update_user({"password": data.password})
    if update_res.get("error"):
        return api_response(error=APIError(message=update_res["error"]["message"]), status_code=400)
    return api_response(data=MagicLinkResponse(message="Password set successfully."), status_code=200)

def login_service(data: LoginRequest):
    res = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    if res.get("error"):
        return api_response(error=APIError(message=res["error"]["message"]), status_code=401)
    session = res.get("session")
    user = res.get("user")
    if not session or not user:
        return api_response(error=APIError(message="Invalid credentials."), status_code=401)
    return api_response(
        data=LoginResponse(
            access_token=session["access_token"],
            token_type="bearer",
            user=user
        ),
        status_code=200
    )

def reset_password_service(data: ResetPasswordRequest):
    res = supabase.auth.reset_password_for_email(data.email)
    if res.get("error"):
        return api_response(error=APIError(message=res["error"]["message"]), status_code=400)
    return api_response(data=ResetPasswordResponse(message="Password reset email sent."), status_code=200)

def register_service(data: RegisterRequest):
    # Puedes adaptar esto para usar supabase.auth.sign_up si lo deseas
    return api_response(
        data=RegisterResponse(
            id="2",
            email=data.email,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name
        ),
        status_code=201
    )

def get_current_user_service(authorization: str):
    if not authorization.startswith("Bearer "):
        return api_response(error=APIError(message="Invalid authorization header"), status_code=401)
    token = authorization.replace("Bearer ", "")
    res = supabase.auth.get_user(token)
    if not res.get("user"):
        return api_response(error=APIError(message="Invalid or expired token"), status_code=401)
    return res["user"] 