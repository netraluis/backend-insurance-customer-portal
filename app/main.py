from fastapi import FastAPI
from fastapi.routing import APIRouter
from app.api import auth, policies, claims, documents

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