from typing import Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class APIError(BaseModel):
    message: str
    details: Optional[str] = None
    hint: Optional[str] = None
    code: Optional[str] = None

class APIResponse(GenericModel, Generic[T]):
    data: Optional[T]
    error: Optional[APIError]
    count: Optional[int]
    status_code: int 