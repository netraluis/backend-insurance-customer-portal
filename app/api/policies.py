from fastapi import APIRouter, Query, Path, Depends
from app.api.auth import get_current_user
from app.models.base import APIResponse, APIError, api_response
from app.models.policy import PolicySummary, PolicyDetail
from typing import List, Optional
from app.services.policy_service import (
    list_policies_service,
    get_policy_service
)

router = APIRouter()

@router.get("", response_model=APIResponse[List[PolicySummary]])
def list_policies(user=Depends(get_current_user),
    type: Optional[str] = Query(None, description="Filter by policy type"),
    status: Optional[str] = Query(None, description="Filter by policy status"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Page size for pagination")
) -> APIResponse[List[PolicySummary]]:
    """
    Returns a list of all user policies with optional filters and pagination (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    return list_policies_service(type, status, page, page_size)

@router.get("/{id}", response_model=APIResponse[PolicyDetail])
def get_policy(id: str, user=Depends(get_current_user)) -> APIResponse[PolicyDetail]:
    """
    Returns details for a specific policy (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    return get_policy_service(id) 