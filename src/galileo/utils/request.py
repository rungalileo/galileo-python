from enum import Enum
from http.client import HTTPException
from typing import Any

from httpx import Response

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient


async def _validate_response(response: Response) -> None:
    if not response.status_code < 300:
        msg = (
            "Something didn't go quite right. The api returned a non-ok status "
            f"code {response.status_code} with output: {response.text}"
        )
        # TODO: Better error handling.
        raise HTTPException(msg)


async def make_request(request_method: RequestMethod, base_url: str, endpoint: str, **kwargs: Any) -> Any:
    return await ApiClient.make_request(request_method=request_method, base_url=base_url, endpoint=endpoint, **kwargs)


class HttpHeaders(str, Enum):
    accept = "accept"
    content_type = "Content-Type"
    application_json = "application/json"

    @staticmethod
    def accept_json() -> dict[str, str]:
        return {HttpHeaders.accept: HttpHeaders.application_json}

    @staticmethod
    def content_type_json() -> dict[str, str]:
        return {HttpHeaders.content_type: HttpHeaders.application_json}

    @staticmethod
    def json() -> dict[str, str]:
        return {**HttpHeaders.accept_json(), **HttpHeaders.content_type_json()}
