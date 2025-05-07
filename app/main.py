from fastapi import FastAPI, Request, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from app.api import auth, policies, claims, documents
from dotenv import load_dotenv
from app.models.base import APIResponse, APIError
import traceback
import logging
from fastapi.middleware.cors import CORSMiddleware
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

api_v1 = APIRouter()

@api_v1.get("/health", tags=["Health"])
def health():
    """Health check endpoint to verify the server is running."""
    return {"status": "ok", "message": "Server is running"}

api_v1.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1.include_router(policies.router, prefix="/policies", tags=["policies"])
api_v1.include_router(claims.router, prefix="/claims", tags=["claims"])
api_v1.include_router(documents.router, prefix="/documents", tags=["documents"])

@api_v1.get("/", tags=["Root"])
def root():
    return {"message": "API Insurance Customer Portal"}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O tu dominio ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1, prefix="/v1")

# Global exception handler for uncaught exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for uncaught exceptions.
    Returns a standardized APIResponse with error details.
    """
    # Log the error with traceback
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())

    # Determine if it's a known error type
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        error_message = exc.detail
    else:
        status_code = 500
        error_message = "Internal Server Error"

    # Create error response
    response = APIResponse(
        data=None,
        error=APIError(
            message=error_message,
            details=str(exc) if status_code != 500 else None,  # Hide details in production for 500 errors
            code="internal_error" if status_code == 500 else "error"
        ),
        count=None,
        status_code=status_code
    )

    return JSONResponse(
        status_code=status_code,
        content=response.dict()
    ) 