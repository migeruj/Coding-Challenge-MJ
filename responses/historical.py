from pydantic import BaseModel
from typing import Any
from enum import Enum

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
    200: {"model": Accepted}
}

class PreconditionError(str, Enum):
    SCHEMA_EMPLOYEES_ERROR = "Check your batch file, Doesn't belong to employees schema"
    SCHEMA_JOBS_ERROR = "Check your batch file, Doesn't belong to jobs schema"
    SCHEMA_DEPARTMENTS_ERROR = "Check your batch file, Doesn't belong to departments schema"
    UNABLE_TO_DEFINE_SCHEMA = "More columns than expected"

class PreconditionFailed(BaseModel):
    detail: str = PreconditionError

PreconditionFailedErrors = {
    412: {"model": PreconditionFailed}
}


Historical_Services_Responses = {**BaseErrors, **Success, **PreconditionFailedErrors}
