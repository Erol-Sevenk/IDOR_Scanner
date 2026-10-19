from pydantic import BaseModel
from enum import Enum
from typing import Optional

class ParamLocation(str, Enum):
    PATH = "path"
    QUERY = "query"
    BODY = "body"

class IDParameter(BaseModel):
    name: str                   # örn. "user_id", "username", "report_id"
    location: ParamLocation
    confidence: float           # 0.0-1.0, ne kadar "ID gibi" olduğu
    example_value: Optional[str] = None

class Endpoint(BaseModel):
    path: str                   # örn. "/users/v1/{username}"
    method: str                 # GET, POST, PUT, DELETE, PATCH
    source: str                 # "openapi" ya da "har"
    id_parameters: list[IDParameter] = []
    raw_headers: dict = {}      # auth header örneği (HAR'dan gelirse)
    body_example: Optional[dict] = None
