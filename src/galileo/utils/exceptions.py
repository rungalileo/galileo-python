from __future__ import annotations

import json
from typing import TYPE_CHECKING

from galileo.resources.types import UNSET

if TYPE_CHECKING:
    from galileo.resources.models import HTTPValidationError


class APIException(Exception):
    """
    APIException is base exception for all API errors. It tries to parse content.detail
    and put it to message.
    """

    def __init__(self, message: str) -> None:
        try:
            self.message = json.loads(message)["detail"]
        except (KeyError, TypeError, ValueError):
            self.message = message
        super().__init__(self.message)


def _format_http_validation_error(error: HTTPValidationError) -> str:
    """Format HTTPValidationError detail list into a human-readable string.

    Parameters
    ----------
    error : HTTPValidationError
        The validation error returned by the API on HTTP 422 responses.

    Returns
    -------
    str
        A human-readable description of all validation failures.
    """
    detail = error.detail
    if detail is UNSET or not detail:
        return "Request validation failed (no details provided)"
    parts = ["[{}] {}".format(".".join(str(p) for p in ve.loc), ve.msg) for ve in detail]
    return "Request validation failed — " + "; ".join(parts)
