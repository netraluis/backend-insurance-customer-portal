from fastapi import APIRouter, Query, Depends
from app.api.auth import get_current_user
from app.models.base import APIResponse, APIError
from app.models.policy import PolicySummary, PolicyDetail
from typing import List, Optional

router = APIRouter()

@router.get("", response_model=APIResponse[List[PolicySummary]])
def list_policies(user=Depends(get_current_user),
    status: Optional[str] = Query(None, description="Filter by policy status"),
    type: Optional[str] = Query(None, description="Filter by policy type"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Page size for pagination")
) -> APIResponse[List[PolicySummary]]:
    """Return a list of all user policies with optional filters and pagination (mocked)."""
    # Filtering and pagination are mocked
    data = [
        PolicySummary(
            id="HOM123",
            contract_name="Home Insurance Basic",
            policy_number="POL123456",
            status="Active",
            payment="$1,200/year",
            next_payment="2024-12-01",
            effective_date="2023-04-15",
            expiration_date="2026-01-15",
            type="home"
        ),
        PolicySummary(
            id="AUT456",
            contract_name="Auto Insurance Plus",
            policy_number="POL654321",
            status="Active",
            payment="$800/year",
            next_payment="2024-10-01",
            effective_date="2023-05-10",
            expiration_date="2025-05-10",
            type="auto"
        )
    ]
    return APIResponse(data=data, error=None, count=len(data), status_code=200)

@router.get("/{id}", response_model=APIResponse[PolicyDetail])
def get_policy(id: str, user=Depends(get_current_user)) -> APIResponse[PolicyDetail]:
    """Return details for a specific policy (mocked)."""
    detail = PolicyDetail(
        id=id,
        contract_name="Home Insurance Basic" if id.startswith("HOM") else "Auto Insurance Plus",
        policy_number="POL123456" if id.startswith("HOM") else "POL654321",
        status="Active",
        payment="$1,200/year" if id.startswith("HOM") else "$800/year",
        payment_frequency="Yearly",
        next_payment="2024-12-01" if id.startswith("HOM") else "2024-10-01",
        effective_date="2023-04-15" if id.startswith("HOM") else "2023-05-10",
        expiration_date="2026-01-15" if id.startswith("HOM") else "2025-05-10",
        manager="Jane Doe",
        type="home" if id.startswith("HOM") else "auto"
    )
    return APIResponse(data=detail, error=None, count=None, status_code=200) 