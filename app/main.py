from fastapi import FastAPI, Request
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from app.api import auth, policies, claims, documents
from dotenv import load_dotenv
from app.models.base import APIResponse, APIError

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
app.include_router(api_v1, prefix="/v1")

# Global exception handler for uncaught exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for uncaught exceptions.
    Returns a standardized APIResponse with error details.
    """
    # You can log the error here if needed
    response = APIResponse(
        data=None,
        error=APIError(
            message="Internal Server Error",
            details=str(exc),  # In production, you might want to hide this
            code="internal_error"
        ),
        count=None,
        status_code=500
    )
    return JSONResponse(
        status_code=500,
        content=response.dict()
    ) 