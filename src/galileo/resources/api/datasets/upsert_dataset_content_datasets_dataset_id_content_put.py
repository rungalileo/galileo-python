from http import HTTPStatus
from typing import Any, Optional, cast

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
from ...models.http_validation_error import HTTPValidationError
from ...models.rollback_request import RollbackRequest
from ...models.upsert_dataset_content_request import UpsertDatasetContentRequest
from ...types import Response


def _get_kwargs(dataset_id: str, *, body: RollbackRequest | UpsertDatasetContentRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PUT,
        "return_raw_response": True,
        "path": "/datasets/{dataset_id}/content".format(dataset_id=dataset_id),
    }

    _kwargs["json"]: dict[str, Any]
    if isinstance(body, RollbackRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Any | HTTPValidationError:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str, *, client: ApiClient, body: RollbackRequest | UpsertDatasetContentRequest
) -> Response[Any | HTTPValidationError]:
    """Upsert Dataset Content

     Rollback the content of a dataset to a previous version.

    Args:
        dataset_id (str):
        body (RollbackRequest | UpsertDatasetContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str, *, client: ApiClient, body: RollbackRequest | UpsertDatasetContentRequest
) -> Optional[Any | HTTPValidationError]:
    """Upsert Dataset Content

     Rollback the content of a dataset to a previous version.

    Args:
        dataset_id (str):
        body (RollbackRequest | UpsertDatasetContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(dataset_id=dataset_id, client=client, body=body).parsed


async def asyncio_detailed(
    dataset_id: str, *, client: ApiClient, body: RollbackRequest | UpsertDatasetContentRequest
) -> Response[Any | HTTPValidationError]:
    """Upsert Dataset Content

     Rollback the content of a dataset to a previous version.

    Args:
        dataset_id (str):
        body (RollbackRequest | UpsertDatasetContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str, *, client: ApiClient, body: RollbackRequest | UpsertDatasetContentRequest
) -> Optional[Any | HTTPValidationError]:
    """Upsert Dataset Content

     Rollback the content of a dataset to a previous version.

    Args:
        dataset_id (str):
        body (RollbackRequest | UpsertDatasetContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (await asyncio_detailed(dataset_id=dataset_id, client=client, body=body)).parsed
