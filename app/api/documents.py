from fastapi import APIRouter, Query, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.api.auth import get_current_user
from app.models.base import APIResponse, APIError, api_response

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
    data = [
        DocumentSummary(
            id="DOC001",
            name="Policy Contract.pdf",
            category="contract",
            policy_id="HOM123",
            claim_id=None,
            billing=None,
            type="pdf"
        ),
        DocumentSummary(
            id="DOC002",
            name="Coverage Certificate.pdf",
            category="certificate",
            policy_id="AUT456",
            claim_id=None,
            billing=None,
            type="pdf"
        )
    ]
    return api_response(data=data, count=len(data), status_code=200)

@router.get("/{id}", response_model=APIResponse[DocumentDetail])
def get_document(id: str, user=Depends(get_current_user)) -> APIResponse[DocumentDetail]:
    """
    Returns details for a specific document (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    detail = DocumentDetail(
        id=id,
        name="Policy Contract.pdf" if id == "DOC001" else "Coverage Certificate.pdf",
        category="contract" if id == "DOC001" else "certificate",
        policy_id="HOM123" if id == "DOC001" else "AUT456",
        claim_id=None,
        billing=None,
        type="pdf",
        url=f"https://example.com/documents/{id}.pdf"
    )
    return api_response(data=detail, status_code=200)

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
    response = DocumentUploadResponse(
        id="DOC999",
        name=name,
        category=category,
        policy_id=policy_id,
        claim_id=claim_id,
        billing=billing,
        type=type,
        url=f"https://example.com/documents/DOC999.pdf"
    )
    return api_response(data=response, status_code=201) 