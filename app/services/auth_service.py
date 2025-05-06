import os
from dotenv import load_dotenv 
load_dotenv()
from supabase import create_client, Client
from app.models.auth import (
    MagicLinkRequest, MagicLinkResponse, SetPasswordRequest, LoginRequest, LoginResponse,
    ResetPasswordRequest, ResetPasswordResponse, RegisterRequest, RegisterResponse, UserResponse,
    ValidationEmailRequest, ValidationEmailResponse, VerifyOTPRequest, VerifyOTPResponse
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

def send_otp_email_service(data: ValidationEmailRequest):
    try:
        res = supabase.auth.sign_in_with_otp({
            "email": data.email,
            "options": {
                "should_create_user": False
            }
        })
        
        # La respuesta de Supabase es un objeto AuthOtpResponse
        if hasattr(res, 'error') and res.error:
            return api_response(error=APIError(message=str(res.error)), status_code=400)
            
        return api_response(
            data=ValidationEmailResponse(
                message="OTP code sent to email.",
                otp_sent=True
            ),
            status_code=200
        )
    except Exception as e:
        return api_response(error=APIError(message=str(e)), status_code=500)

def verify_otp_service(data: VerifyOTPRequest):
    try:
        res = supabase.auth.verify_otp({
            "email": data.email,
            "token": data.token,
            "type": "email"
        })
        
        if hasattr(res, 'error') and res.error:
            return api_response(error=APIError(message=str(res.error)), status_code=400)
            
        # If verification is successful, return session data
        session = res.session if hasattr(res, 'session') else None
        user = res.user if hasattr(res, 'user') else None
        
        # Convert user data to dict and handle datetime serialization
        user_dict = None
        if user:
            user_dict = user.dict()
            # Convert all datetime fields to ISO format strings
            datetime_fields = [
                'created_at', 'updated_at', 'last_sign_in_at', 'confirmed_at',
                'email_confirmed_at', 'phone_confirmed_at', 'recovery_sent_at',
                'email_change_sent_at', 'invited_at'
            ]
            
            for field in datetime_fields:
                if field in user_dict and user_dict[field]:
                    user_dict[field] = user_dict[field].isoformat()
            
            # Handle identities datetime fields
            if 'identities' in user_dict and user_dict['identities']:
                for identity in user_dict['identities']:
                    if isinstance(identity, dict):
                        for field in ['created_at', 'last_sign_in_at', 'updated_at']:
                            if field in identity and identity[field]:
                                identity[field] = identity[field].isoformat()
        
        return api_response(
            data=VerifyOTPResponse(
                message="OTP verified successfully.",
                access_token=session.access_token if session else None,
                token_type="bearer" if session else None,
                user=user_dict
            ),
            status_code=200
        )
    except Exception as e:
        return api_response(error=APIError(message=str(e)), status_code=500) 