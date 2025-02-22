from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.rollback_request import RollbackRequest
from ...types import Response


def _get_kwargs(dataset_id: str, *, body: RollbackRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "put", "url": f"/datasets/{dataset_id}/content"}

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
    dataset_id: str, *, client: AuthenticatedClient, body: RollbackRequest
) -> Response[Union[Any, HTTPValidationError]]:
    """Rollback Dataset Content

     Rollback the content of a dataset to a previous version.

    Args:
        dataset_id (str):
        body (RollbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str, *, client: AuthenticatedClient, body: RollbackRequest
) -> Optional[Union[Any, HTTPValidationError]]:
    """Rollback Dataset Content

     Rollback the content of a dataset to a previous version.

    Args:
        dataset_id (str):
        body (RollbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(dataset_id=dataset_id, client=client, body=body).parsed


async def asyncio_detailed(
    dataset_id: str, *, client: AuthenticatedClient, body: RollbackRequest
) -> Response[Union[Any, HTTPValidationError]]:
    """Rollback Dataset Content

     Rollback the content of a dataset to a previous version.

    Args:
        dataset_id (str):
        body (RollbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str, *, client: AuthenticatedClient, body: RollbackRequest
) -> Optional[Union[Any, HTTPValidationError]]:
    """Rollback Dataset Content

     Rollback the content of a dataset to a previous version.

    Args:
        dataset_id (str):
        body (RollbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (await asyncio_detailed(dataset_id=dataset_id, client=client, body=body)).parsed
