from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any = None


def success_response(
    data: Any = None,
    message: str = "Request successful",
) -> APIResponse:
    return APIResponse(
        success=True,
        message=message,
        data=data,
    )