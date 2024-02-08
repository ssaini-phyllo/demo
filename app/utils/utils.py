from http import HTTPStatus
from typing import Optional


class RequestError(Exception):
    def __init__(self, status_code: int, error_code: str, error_msg: Optional[str] = None):
        self.status_code = HTTPStatus(status_code)
        self.error_code = error_code
        self.error_msg = error_msg


class ErrorCode:
    INVALID_ID = "INVALID_ID"
    INVALID_USER_ID = "INVALID_USER_ID"
    INVALID_NAME = "INVALID_NAME"
    INVALID_START_DATE = "INVALID_START_DATE"
    INVALID_END_DATE = "INVALID_END_DATE"
