from fastapi import APIRouter, Query, Path, Depends
from app.api.auth import get_current_user
from app.models.base import APIResponse, APIError, api_response
from app.models.claim import ClaimSummary, ClaimDetail, ClaimCreateRequest, ClaimCreateResponse
from typing import List, Optional

router = APIRouter()

@router.get("", response_model=APIResponse[List[ClaimSummary]])
def list_claims(user=Depends(get_current_user),
    policy_id: Optional[str] = Query(None, description="Filter by policy id"),
    status: Optional[str] = Query(None, description="Filter by claim status"),
    type: Optional[str] = Query(None, description="Filter by claim type"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Page size for pagination")
) -> APIResponse[List[ClaimSummary]]:
    """
    Returns a list of all user claims with optional filters and pagination (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    data = [
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
    # Optionally filter by policy_id
    if policy_id:
        data = [c for c in data if c.policy_id == policy_id]
    return api_response(data=data, count=len(data), status_code=200)

@router.get("/{id}", response_model=APIResponse[ClaimDetail])
def get_claim(id: str, user=Depends(get_current_user)) -> APIResponse[ClaimDetail]:
    """
    Returns details for a specific claim (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    detail = ClaimDetail(
        id=id,
        claim_number=id,
        status="Open" if id == "CLM001" else "Closed",
        open_date="2024-05-01" if id == "CLM001" else "2024-04-10",
        description="Water damage in kitchen" if id == "CLM001" else "Minor collision",
        policy_id="HOM123" if id == "CLM001" else "AUT456",
        contract_name="Home Insurance Basic" if id == "CLM001" else "Auto Insurance Plus"
    )
    return api_response(data=detail, status_code=200)

@router.post("", response_model=APIResponse[ClaimCreateResponse])
def create_claim(data: ClaimCreateRequest, user=Depends(get_current_user)) -> APIResponse[ClaimCreateResponse]:
    """
    Creates a new claim (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    response = ClaimCreateResponse(
        id="CLM999",
        claim_number="CLM999",
        status="Open",
        open_date=data.open_date or "2024-06-01",
        description=data.description,
        policy_id=data.policy_id,
        contract_name="Home Insurance Basic" if data.policy_id == "HOM123" else "Auto Insurance Plus"
    )
    return api_response(data=response, status_code=201)
