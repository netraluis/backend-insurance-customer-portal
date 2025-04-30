from fastapi import APIRouter, Query, Path, Depends
from app.api.auth import get_current_user
from app.models.base import APIResponse, APIError, api_response
from app.models.policy import PolicySummary, PolicyDetail
from typing import List, Optional

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
    data = [
        PolicySummary(
            id="HOM123",
            policy_number="HOM123",
            type="Home",
            status="Active",
            start_date="2024-01-01",
            end_date="2025-01-01",
            contract_name="Home Insurance Basic"
        ),
        PolicySummary(
            id="AUT456",
            policy_number="AUT456",
            type="Auto",
            status="Expired",
            start_date="2023-01-01",
            end_date="2024-01-01",
            contract_name="Auto Insurance Plus"
        )
    ]
    if type:
        data = [p for p in data if p.type == type]
    if status:
        data = [p for p in data if p.status == status]
    return api_response(data=data, count=len(data), status_code=200)

@router.get("/{id}", response_model=APIResponse[PolicyDetail])
def get_policy(id: str, user=Depends(get_current_user)) -> APIResponse[PolicyDetail]:
    """
    Returns details for a specific policy (mocked).
    Uses api_response to ensure the HTTP status code matches the status_code in the response body.
    """
    detail = PolicyDetail(
        id=id,
        policy_number=id,
        type="Home" if id == "HOM123" else "Auto",
        status="Active" if id == "HOM123" else "Expired",
        start_date="2024-01-01" if id == "HOM123" else "2023-01-01",
        end_date="2025-01-01" if id == "HOM123" else "2024-01-01",
        contract_name="Home Insurance Basic" if id == "HOM123" else "Auto Insurance Plus",
        coverage_amount=100000.0 if id == "HOM123" else 20000.0,
        premium=500.0 if id == "HOM123" else 300.0,
        deductible=1000.0 if id == "HOM123" else 500.0
    )
    return api_response(data=detail, status_code=200) 