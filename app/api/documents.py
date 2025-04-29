from fastapi import APIRouter, Query, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional

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

@router.get("", response_model=List[DocumentSummary])
def list_documents(
    policy_id: Optional[str] = Query(None, description="Filter by policy id"),
    claim_id: Optional[str] = Query(None, description="Filter by claim id"),
    billing: Optional[str] = Query(None, description="Filter by billing"),
    type: Optional[str] = Query(None, description="Filter by document type"),
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Page size for pagination")
) -> List[DocumentSummary]:
    """Return a list of all user documents with optional filters and pagination (mocked)."""
    return [
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

@router.get("/{id}", response_model=DocumentDetail)
def get_document(id: str) -> DocumentDetail:
    """Return details for a specific document (mocked)."""
    return DocumentDetail(
        id=id,
        name="Policy Contract.pdf" if id == "DOC001" else "Coverage Certificate.pdf",
        category="contract" if id == "DOC001" else "certificate",
        policy_id="HOM123" if id == "DOC001" else "AUT456",
        claim_id=None,
        billing=None,
        type="pdf",
        url=f"https://example.com/documents/{id}.pdf"
    )

@router.post("", response_model=DocumentUploadResponse)
def upload_document(
    file: UploadFile = File(...),
    name: str = Query(...),
    category: str = Query(...),
    policy_id: Optional[str] = Query(None),
    claim_id: Optional[str] = Query(None),
    billing: Optional[str] = Query(None),
    type: str = Query(...)
) -> DocumentUploadResponse:
    """Upload a new document (mocked)."""
    return DocumentUploadResponse(
        id="DOC999",
        name=name,
        category=category,
        policy_id=policy_id,
        claim_id=claim_id,
        billing=billing,
        type=type,
        url=f"https://example.com/documents/DOC999.pdf"
    ) 