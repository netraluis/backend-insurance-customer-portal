from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.api.auth import get_current_user

router = APIRouter()

class PolicySummary(BaseModel):
    id: str
    contract_name: str
    policy_number: str
    status: str
    payment: str
    next_payment: Optional[str]
    effective_date: str
    expiration_date: str
    type: str

class PolicyDetail(BaseModel):
    id: str
    contract_name: str
    policy_number: str
    status: str
    payment: str
    payment_frequency: str
    next_payment: Optional[str]
    effective_date: str
    expiration_date: str
    manager: str
    type: str

@router.get("", response_model=List[PolicySummary])
def list_policies(user=Depends(get_current_user),
    status: Optional[str] = Query(None, description="Filter by policy status"),
    type: Optional[str] = Query(None, description="Filter by policy type"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Page size for pagination")
) -> List[PolicySummary]:
    """Return a list of all user policies with optional filters and pagination (mocked)."""
    # Filtering and pagination are mocked
    return [
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

@router.get("/{id}", response_model=PolicyDetail)
def get_policy(id: str, user=Depends(get_current_user)) -> PolicyDetail:
    """Return details for a specific policy (mocked)."""
    return PolicyDetail(
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