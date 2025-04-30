from fastapi import APIRouter, Query, Path, Depends
from app.api.auth import get_current_user
from app.models.base import APIResponse, APIError, api_response
from app.models.claim import ClaimSummary, ClaimDetail, ClaimCreateRequest, ClaimCreateResponse
from typing import List, Optional
from app.services.claim_service import (
    list_claims_service,
    get_claim_service,
    create_claim_service
)

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
    return list_claims_service(policy_id, status, type, page, page_size)

@router.get("/{id}", response_model=APIResponse[ClaimDetail])
def get_claim(id: str, user=Depends(get_current_user)) -> APIResponse[ClaimDetail]:
    """
    Returns details for a specific claim (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    return get_claim_service(id)

@router.post("", response_model=APIResponse[ClaimCreateResponse])
def create_claim(data: ClaimCreateRequest, user=Depends(get_current_user)) -> APIResponse[ClaimCreateResponse]:
    """
    Creates a new claim (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    return create_claim_service(data)
