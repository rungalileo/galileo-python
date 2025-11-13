from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(*, catalog: Union[None, Unset, str] = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_catalog: Union[None, Unset, str]
    json_catalog = UNSET if isinstance(catalog, Unset) else catalog
    params["catalog"] = json_catalog

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/integrations/databricks/databases",
        "params": params,
    }

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[Union[HTTPValidationError, list[str]]]:
    if response.status_code == 200:
        return cast(list[str], response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[HTTPValidationError, list[str]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, catalog: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Databases For Cluster.

    Args:
        catalog (Union[None, Unset, str]):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, list[str]]]
    """
    kwargs = _get_kwargs(catalog=catalog)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, catalog: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Databases For Cluster.

    Args:
        catalog (Union[None, Unset, str]):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, list[str]]
    """
    return sync_detailed(client=client, catalog=catalog).parsed


async def asyncio_detailed(
    *, client: ApiClient, catalog: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Databases For Cluster.

    Args:
        catalog (Union[None, Unset, str]):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, list[str]]]
    """
    kwargs = _get_kwargs(catalog=catalog)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, catalog: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Databases For Cluster.

    Args:
        catalog (Union[None, Unset, str]):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, list[str]]
    """
    return (await asyncio_detailed(client=client, catalog=catalog)).parsed
