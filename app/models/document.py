from pydantic import BaseModel
from typing import Optional

class DocumentSummary(BaseModel):
    id: str
    name: str
    category: str
    policy_id: Optional[str]
    claim_id: Optional[str]
    billing: Optional[str]
    type: str

class DocumentDetail(BaseModel):
    id: str
    name: str
    category: str
    policy_id: Optional[str]
    claim_id: Optional[str]
    billing: Optional[str]
    type: str
    url: str

class DocumentUploadRequest(BaseModel):
    name: str
    category: str
    policy_id: Optional[str]
    claim_id: Optional[str]
    billing: Optional[str]
    type: str

class DocumentUploadResponse(BaseModel):
    id: str
    name: str
    category: str
    policy_id: Optional[str]
    claim_id: Optional[str]
    billing: Optional[str]
    type: str
    url: str 