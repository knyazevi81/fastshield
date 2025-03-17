from fastapi.exceptions import HTTPException
from fastapi import status


class HackException(HTTPException):
    status=status.HTTP_423_LOCKED
    detail="request has been blocked"
