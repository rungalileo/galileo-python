from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(scorer_id: str, *, version: Union[None, Unset, int] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_version: Union[None, Unset, int]
    if isinstance(version, Unset):
        json_version = UNSET
    else:
        json_version = version
    params["version"] = json_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/scorers/{scorer_id}/version/code", "params": params}

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
    scorer_id: str, *, client: AuthenticatedClient, version: Union[None, Unset, int] = UNSET
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Scorer Version Code

    Args:
        scorer_id (str):
        version (Union[None, Unset, int]): version number, defaults to latest version

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id, version=version)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    scorer_id: str, *, client: AuthenticatedClient, version: Union[None, Unset, int] = UNSET
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Scorer Version Code

    Args:
        scorer_id (str):
        version (Union[None, Unset, int]): version number, defaults to latest version

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(scorer_id=scorer_id, client=client, version=version).parsed


async def asyncio_detailed(
    scorer_id: str, *, client: AuthenticatedClient, version: Union[None, Unset, int] = UNSET
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Scorer Version Code

    Args:
        scorer_id (str):
        version (Union[None, Unset, int]): version number, defaults to latest version

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id, version=version)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scorer_id: str, *, client: AuthenticatedClient, version: Union[None, Unset, int] = UNSET
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Scorer Version Code

    Args:
        scorer_id (str):
        version (Union[None, Unset, int]): version number, defaults to latest version

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (await asyncio_detailed(scorer_id=scorer_id, client=client, version=version)).parsed
