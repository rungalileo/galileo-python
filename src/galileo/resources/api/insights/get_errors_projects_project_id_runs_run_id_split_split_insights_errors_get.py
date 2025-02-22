from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...types import Response


def _get_kwargs(project_id: str, run_id: str, split: Split) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/insights/errors",
    }

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
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Errors

     Get the available errors for a run (if any)

    Args:
        project_id (str):
        run_id (str):
        split (Split):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list[str]]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Errors

     Get the available errors for a run (if any)

    Args:
        project_id (str):
        run_id (str):
        split (Split):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list[str]]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, split=split, client=client).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Errors

     Get the available errors for a run (if any)

    Args:
        project_id (str):
        run_id (str):
        split (Split):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list[str]]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Errors

     Get the available errors for a run (if any)

    Args:
        project_id (str):
        run_id (str):
        split (Split):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list[str]]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, split=split, client=client)).parsed
