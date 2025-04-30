from app.models.base import APIResponse, api_response
from app.models.claim import ClaimSummary, ClaimDetail, ClaimCreateRequest, ClaimCreateResponse
from typing import List, Optional

def list_claims_service(policy_id: Optional[str], status: Optional[str], type: Optional[str], page: int, page_size: int) -> APIResponse[List[ClaimSummary]]:
    # TODO: Implement logic to fetch and filter claims from the database or external service.
    # Should support filtering by policy_id, status, type, and pagination (page, page_size).
    # Return a list of ClaimSummary objects and the total count.
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
    if policy_id:
        data = [c for c in data if c.policy_id == policy_id]
    return api_response(data=data, count=len(data), status_code=200)

def get_claim_service(id: str) -> APIResponse[ClaimDetail]:
    # TODO: Implement logic to fetch a specific claim by its ID from the database or external service.
    # Should return a ClaimDetail object if found, or an appropriate error if not found.
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

def create_claim_service(data: ClaimCreateRequest) -> APIResponse[ClaimCreateResponse]:
    # TODO: Implement logic to create a new claim in the database or external service.
    # Should validate the input, persist the claim, and return the created ClaimCreateResponse object.
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