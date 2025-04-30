from app.models.base import APIResponse, api_response
from app.models.policy import PolicySummary, PolicyDetail
from typing import List, Optional

def list_policies_service(type: Optional[str], status: Optional[str], page: int, page_size: int) -> APIResponse[List[PolicySummary]]:
    # TODO: Implement logic to fetch and filter policies from the database or external service.
    # Should support filtering by type, status, and pagination (page, page_size).
    # Return a list of PolicySummary objects and the total count.
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

def get_policy_service(id: str) -> APIResponse[PolicyDetail]:
    # TODO: Implement logic to fetch a specific policy by its ID from the database or external service.
    # Should return a PolicyDetail object if found, or an appropriate error if not found.
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