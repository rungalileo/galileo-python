from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(*, catalog: Union[None, Unset, str] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_catalog: Union[None, Unset, str]
    if isinstance(catalog, Unset):
        json_catalog = UNSET
    else:
        json_catalog = catalog
    params["catalog"] = json_catalog

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": "/integrations/databricks/databases", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list[str]]]:
    if response.status_code == 200:
        response_200 = cast(list[str], response.json())

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
) -> Response[Union[HTTPValidationError, list[str]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, catalog: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Databases For Cluster

    Args:
        catalog (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list[str]]]
    """

    kwargs = _get_kwargs(catalog=catalog)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, catalog: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Databases For Cluster

    Args:
        catalog (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list[str]]
    """

    return sync_detailed(client=client, catalog=catalog).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, catalog: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Databases For Cluster

    Args:
        catalog (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list[str]]]
    """

    kwargs = _get_kwargs(catalog=catalog)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, catalog: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Databases For Cluster

    Args:
        catalog (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list[str]]
    """

    return (await asyncio_detailed(client=client, catalog=catalog)).parsed
