from fastapi import APIRouter, Query, Path, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.api.auth import get_current_user

router = APIRouter()

class ClaimSummary(BaseModel):
    id: str
    claim_number: str
    status: str
    open_date: str
    description: str
    policy_id: str
    contract_name: str

class ClaimDetail(BaseModel):
    id: str
    claim_number: str
    status: str
    open_date: str
    description: str
    policy_id: str
    contract_name: str

class ClaimCreateRequest(BaseModel):
    description: str
    open_date: Optional[str] = None

class ClaimCreateResponse(BaseModel):
    id: str
    claim_number: str
    status: str
    open_date: str
    description: str
    policy_id: str
    contract_name: str

@router.get("", response_model=List[ClaimSummary])
def list_claims(user=Depends(get_current_user),
    policy_id: Optional[str] = Query(None, description="Filter by policy id"),
    status: Optional[str] = Query(None, description="Filter by claim status"),
    type: Optional[str] = Query(None, description="Filter by claim type"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Page size for pagination")
) -> List[ClaimSummary]:
    """Return a list of all user claims with optional filters and pagination (mocked)."""
    return [
        ClaimSummary(
            id="CLM001",
            claim_number="CLM001",
            status="Open",
            open_date="2024-05-01",
            description="Water damage in kitchen",
            policy_id="HOM123",
            contract_name="Home Insurance Basic"
        ),
        ClaimSummary(
            id="CLM002",
            claim_number="CLM002",
            status="Closed",
            open_date="2024-04-10",
            description="Minor collision",
            policy_id="AUT456",
            contract_name="Auto Insurance Plus"
        )
    ]

@router.get("/{id}", response_model=ClaimDetail)
def get_claim(id: str, user=Depends(get_current_user)) -> ClaimDetail:
    """Return details for a specific claim (mocked)."""
    return ClaimDetail(
        id=id,
        claim_number=id,
        status="Open" if id == "CLM001" else "Closed",
        open_date="2024-05-01" if id == "CLM001" else "2024-04-10",
        description="Water damage in kitchen" if id == "CLM001" else "Minor collision",
        policy_id="HOM123" if id == "CLM001" else "AUT456",
        contract_name="Home Insurance Basic" if id == "CLM001" else "Auto Insurance Plus"
    )

@router.post("/policies/{policy_id}/claims", response_model=ClaimCreateResponse)
def create_claim(policy_id: str = Path(..., description="Policy ID to which the claim belongs"),
    data: ClaimCreateRequest = ..., user=Depends(get_current_user)) -> ClaimCreateResponse:
    """Create a new claim for a given policy (mocked)."""
    return ClaimCreateResponse(
        id="CLM999",
        claim_number="CLM999",
        status="Open",
        open_date=data.open_date or "2024-06-01",
        description=data.description,
        policy_id=policy_id,
        contract_name="Home Insurance Basic" if policy_id == "HOM123" else "Auto Insurance Plus"
    ) 