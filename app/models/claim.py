from pydantic import BaseModel
from typing import Optional

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