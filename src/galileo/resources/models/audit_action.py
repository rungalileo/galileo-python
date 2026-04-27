from enum import Enum


class AuditAction(str, Enum):
    ACCOUNT_LOCKOUT = "account_lockout"
    FAILED_LOGIN = "failed_login"
    HTTP_REQUEST = "http_request"
    LOGIN = "login"
    LOGOUT = "logout"
    REFRESH_TOKEN = "refresh_token"
    RESOURCE = "resource"

    def __str__(self) -> str:
        return str(self.value)
