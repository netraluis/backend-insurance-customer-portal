from fastapi import APIRouter, Query, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.api.auth import get_current_user
from app.models.base import APIResponse, APIError, api_response
from app.services.document_service import (
    list_documents_service,
    get_document_service,
    upload_document_service
)

router = APIRouter()

class DocumentSummary(BaseModel):
    id: str
    name: str
    category: str
    policy_id: Optional[str]
    claim_id: Optional[str]
    billing: Optional[str]
    type: str

class DocumentDetail(BaseModel):
    id: str
    name: str
    category: str
    policy_id: Optional[str]
    claim_id: Optional[str]
    billing: Optional[str]
    type: str
    url: str

class DocumentUploadRequest(BaseModel):
    name: str
    category: str
    policy_id: Optional[str]
    claim_id: Optional[str]
    billing: Optional[str]
    type: str

class DocumentUploadResponse(BaseModel):
    id: str
    name: str
    category: str
    policy_id: Optional[str]
    claim_id: Optional[str]
    billing: Optional[str]
    type: str
    url: str

@router.get("", response_model=APIResponse[List[DocumentSummary]])
def list_documents(user=Depends(get_current_user),
    policy_id: Optional[str] = Query(None, description="Filter by policy id"),
    claim_id: Optional[str] = Query(None, description="Filter by claim id"),
    billing: Optional[str] = Query(None, description="Filter by billing"),
    type: Optional[str] = Query(None, description="Filter by document type"),
    category: Optional[str] = Query(None, description="Filter by document category"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Page size for pagination")
) -> APIResponse[List[DocumentSummary]]:
    """
    Returns a list of all user documents with optional filters and pagination (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    return list_documents_service(policy_id, claim_id, billing, type, category, page, page_size)

@router.get("/{id}", response_model=APIResponse[DocumentDetail])
def get_document(id: str, user=Depends(get_current_user)) -> APIResponse[DocumentDetail]:
    """
    Returns details for a specific document (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    return get_document_service(id)

@router.post("", response_model=APIResponse[DocumentUploadResponse])
def upload_document(file: UploadFile = File(...),
    name: str = Query(...),
    category: str = Query(...),
    policy_id: Optional[str] = Query(None),
    claim_id: Optional[str] = Query(None),
    billing: Optional[str] = Query(None),
    type: str = Query(...),
    user=Depends(get_current_user)) -> APIResponse[DocumentUploadResponse]:
    """
    Uploads a new document (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    return upload_document_service(file, name, category, policy_id, claim_id, billing, type) 