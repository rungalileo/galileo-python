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
from ...models.body_create_dataset_public_v2_datasets_post import BodyCreateDatasetPublicV2DatasetsPost
from ...models.dataset_db import DatasetDB
from ...models.dataset_format import DatasetFormat
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BodyCreateDatasetPublicV2DatasetsPost | Unset,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_format_: str | Unset = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params["hidden"] = hidden

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/public/v2/datasets",
        "params": params,
    }

    if not isinstance(body, Unset):
        _kwargs["files"] = body.to_multipart()

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> DatasetDB | HTTPValidationError:
    if response.status_code == 200:
        response_200 = DatasetDB.from_dict(response.json())

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[DatasetDB | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: ApiClient,
    body: BodyCreateDatasetPublicV2DatasetsPost | Unset,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> Response[DatasetDB | HTTPValidationError]:
    """Create Dataset

     Creates a standalone dataset.

    Args:
        format_ (DatasetFormat | Unset):
        hidden (bool | Unset):  Default: False.
        body (BodyCreateDatasetPublicV2DatasetsPost | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetDB | HTTPValidationError]
    """

    kwargs = _get_kwargs(body=body, format_=format_, hidden=hidden)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: ApiClient,
    body: BodyCreateDatasetPublicV2DatasetsPost | Unset,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> Optional[DatasetDB | HTTPValidationError]:
    """Create Dataset

     Creates a standalone dataset.

    Args:
        format_ (DatasetFormat | Unset):
        hidden (bool | Unset):  Default: False.
        body (BodyCreateDatasetPublicV2DatasetsPost | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetDB | HTTPValidationError
    """

    return sync_detailed(client=client, body=body, format_=format_, hidden=hidden).parsed


async def asyncio_detailed(
    *,
    client: ApiClient,
    body: BodyCreateDatasetPublicV2DatasetsPost | Unset,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> Response[DatasetDB | HTTPValidationError]:
    """Create Dataset

     Creates a standalone dataset.

    Args:
        format_ (DatasetFormat | Unset):
        hidden (bool | Unset):  Default: False.
        body (BodyCreateDatasetPublicV2DatasetsPost | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetDB | HTTPValidationError]
    """

    kwargs = _get_kwargs(body=body, format_=format_, hidden=hidden)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: ApiClient,
    body: BodyCreateDatasetPublicV2DatasetsPost | Unset,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> Optional[DatasetDB | HTTPValidationError]:
    """Create Dataset

     Creates a standalone dataset.

    Args:
        format_ (DatasetFormat | Unset):
        hidden (bool | Unset):  Default: False.
        body (BodyCreateDatasetPublicV2DatasetsPost | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetDB | HTTPValidationError
    """

    return (await asyncio_detailed(client=client, body=body, format_=format_, hidden=hidden)).parsed
