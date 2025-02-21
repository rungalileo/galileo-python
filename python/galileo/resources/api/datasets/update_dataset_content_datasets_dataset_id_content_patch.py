from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.update_dataset_content_request import UpdateDatasetContentRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str, *, body: UpdateDatasetContentRequest, if_match: Union[None, Unset, str] = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(if_match, Unset):
        headers["If-Match"] = if_match

    _kwargs: dict[str, Any] = {"method": "patch", "url": f"/datasets/{dataset_id}/content"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateDatasetContentRequest,
    if_match: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Update Dataset Content

     Update the content of a dataset.

    The `index` and `column_name` fields are treated as keys tied to a specific version of the dataset.
    As such, these values are considered immutable identifiers for the dataset's structure.

    For example, if an edit operation changes the name of a column, subsequent edit operations in
    the same request should reference the column using its original name.

    The `If-Match` header is used to ensure that updates are only applied if the client's version of the
    dataset
    matches the server's version. This prevents conflicts from simultaneous updates. The `ETag` header
    in the response
    provides the new version identifier after a successful update.

    Args:
        dataset_id (str):
        if_match (Union[None, Unset, str]): ETag of the dataset as a version identifier.
        body (UpdateDatasetContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, body=body, if_match=if_match)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateDatasetContentRequest,
    if_match: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Update Dataset Content

     Update the content of a dataset.

    The `index` and `column_name` fields are treated as keys tied to a specific version of the dataset.
    As such, these values are considered immutable identifiers for the dataset's structure.

    For example, if an edit operation changes the name of a column, subsequent edit operations in
    the same request should reference the column using its original name.

    The `If-Match` header is used to ensure that updates are only applied if the client's version of the
    dataset
    matches the server's version. This prevents conflicts from simultaneous updates. The `ETag` header
    in the response
    provides the new version identifier after a successful update.

    Args:
        dataset_id (str):
        if_match (Union[None, Unset, str]): ETag of the dataset as a version identifier.
        body (UpdateDatasetContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(dataset_id=dataset_id, client=client, body=body, if_match=if_match).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateDatasetContentRequest,
    if_match: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Update Dataset Content

     Update the content of a dataset.

    The `index` and `column_name` fields are treated as keys tied to a specific version of the dataset.
    As such, these values are considered immutable identifiers for the dataset's structure.

    For example, if an edit operation changes the name of a column, subsequent edit operations in
    the same request should reference the column using its original name.

    The `If-Match` header is used to ensure that updates are only applied if the client's version of the
    dataset
    matches the server's version. This prevents conflicts from simultaneous updates. The `ETag` header
    in the response
    provides the new version identifier after a successful update.

    Args:
        dataset_id (str):
        if_match (Union[None, Unset, str]): ETag of the dataset as a version identifier.
        body (UpdateDatasetContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, body=body, if_match=if_match)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateDatasetContentRequest,
    if_match: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Update Dataset Content

     Update the content of a dataset.

    The `index` and `column_name` fields are treated as keys tied to a specific version of the dataset.
    As such, these values are considered immutable identifiers for the dataset's structure.

    For example, if an edit operation changes the name of a column, subsequent edit operations in
    the same request should reference the column using its original name.

    The `If-Match` header is used to ensure that updates are only applied if the client's version of the
    dataset
    matches the server's version. This prevents conflicts from simultaneous updates. The `ETag` header
    in the response
    provides the new version identifier after a successful update.

    Args:
        dataset_id (str):
        if_match (Union[None, Unset, str]): ETag of the dataset as a version identifier.
        body (UpdateDatasetContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (await asyncio_detailed(dataset_id=dataset_id, client=client, body=body, if_match=if_match)).parsed
