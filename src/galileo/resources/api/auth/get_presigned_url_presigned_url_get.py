from http import HTTPStatus
from typing import Any, Optional

import httpx

from galileo.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.get_presigned_url_response import GetPresignedUrlResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.method import Method
from ...types import UNSET, Response


def _get_kwargs(*, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["api_url"] = api_url

    json_method = method.value
    params["method"] = json_method

    params["bucket_name"] = bucket_name

    params["object_name"] = object_name

    params["project_id"] = project_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/presigned_url",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> GetPresignedUrlResponse | HTTPValidationError:
    if response.status_code == 200:
        response_200 = GetPresignedUrlResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    # Handle common HTTP errors with actionable messages
    if response.status_code == 400:
        raise BadRequestError(response.status_code, response.content)
    if response.status_code == 401:
        raise AuthenticationError(response.status_code, response.content)
    if response.status_code == 403:
        raise ForbiddenError(response.status_code, response.content)
    if response.status_code == 404:
        raise NotFoundError(response.status_code, response.content)
    if response.status_code == 409:
        raise ConflictError(response.status_code, response.content)
    if response.status_code == 429:
        raise RateLimitError(response.status_code, response.content)
    if response.status_code >= 500:
        raise ServerError(response.status_code, response.content)
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[GetPresignedUrlResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str
) -> Response[GetPresignedUrlResponse | HTTPValidationError]:
    """Get Presigned Url

    Args:
        api_url (str):
        method (Method):
        bucket_name (str):
        object_name (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPresignedUrlResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        api_url=api_url, method=method, bucket_name=bucket_name, object_name=object_name, project_id=project_id
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str
) -> Optional[GetPresignedUrlResponse | HTTPValidationError]:
    """Get Presigned Url

    Args:
        api_url (str):
        method (Method):
        bucket_name (str):
        object_name (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPresignedUrlResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        api_url=api_url,
        method=method,
        bucket_name=bucket_name,
        object_name=object_name,
        project_id=project_id,
    ).parsed


async def asyncio_detailed(
    *, client: ApiClient, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str
) -> Response[GetPresignedUrlResponse | HTTPValidationError]:
    """Get Presigned Url

    Args:
        api_url (str):
        method (Method):
        bucket_name (str):
        object_name (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPresignedUrlResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        api_url=api_url, method=method, bucket_name=bucket_name, object_name=object_name, project_id=project_id
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str
) -> Optional[GetPresignedUrlResponse | HTTPValidationError]:
    """Get Presigned Url

    Args:
        api_url (str):
        method (Method):
        bucket_name (str):
        object_name (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPresignedUrlResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            api_url=api_url,
            method=method,
            bucket_name=bucket_name,
            object_name=object_name,
            project_id=project_id,
        )
    ).parsed
