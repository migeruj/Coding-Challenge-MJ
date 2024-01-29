from pydantic import BaseModel
from typing import Any

class ServerError(BaseModel):
    detail: str = "Server Error"

class NotFound(BaseModel):
    detail: str = "Resource Not found"

class Unprocessable(BaseModel):
    detail: list[dict[str, Any]]

BaseErrors = {
    500: {"model": ServerError},
    404: {"model": NotFound},
    422: {"model": Unprocessable}
}


class Accepted(BaseModel):
    message: str = 'Accepted'

Success = {
    201: {"model": Accepted}
}

Historical_Services_Responses = {**BaseErrors, **Success}
