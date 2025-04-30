from typing import Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel
from fastapi.responses import JSONResponse

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


def api_response(*, data=None, error=None, count=None, status_code=200):
    """
    Helper to return a standardized APIResponse as a JSONResponse,
    ensuring the HTTP status code matches the status_code in the response body.
    Usage:
        return api_response(data=..., status_code=201)
        return api_response(error=APIError(message="..."), status_code=401)
    """
    response = APIResponse(data=data, error=error, count=count, status_code=status_code)
    return JSONResponse(status_code=status_code, content=response.dict()) 