from fastapi.exceptions import HTTPException
from fastapi import status


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class RateLimitException(BaseHTTPException):
    status=status.HTTP_409_CONFLICT
    detail="Request has been blocked"


class HardBlockException(BaseHTTPException):
    status=status.HTTP_409_CONFLICT
    detail="Request has been blocked"


class HackBlockException(BaseHTTPException):
    status=status.HTTP_409_CONFLICT
    detail="Request has been blocked"