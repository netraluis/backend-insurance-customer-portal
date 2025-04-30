from pydantic import BaseModel
from typing import Optional

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