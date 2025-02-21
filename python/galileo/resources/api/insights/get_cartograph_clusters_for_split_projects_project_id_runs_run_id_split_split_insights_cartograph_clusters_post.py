from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cartograph_cluster_response import CartographClusterResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, run_id: str, split: Split, *, inference_name: Union[Unset, str] = ""
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["inference_name"] = inference_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/insights/cartograph_clusters",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CartographClusterResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = CartographClusterResponse.from_dict(response.json())

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
) -> Response[Union[CartographClusterResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient, inference_name: Union[Unset, str] = ""
) -> Response[Union[CartographClusterResponse, HTTPValidationError]]:
    """Get Cartograph Clusters For Split

     Get information about the Cartograph clusters found for a split.

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CartographClusterResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split, inference_name=inference_name)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient, inference_name: Union[Unset, str] = ""
) -> Optional[Union[CartographClusterResponse, HTTPValidationError]]:
    """Get Cartograph Clusters For Split

     Get information about the Cartograph clusters found for a split.

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CartographClusterResponse, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id, run_id=run_id, split=split, client=client, inference_name=inference_name
    ).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient, inference_name: Union[Unset, str] = ""
) -> Response[Union[CartographClusterResponse, HTTPValidationError]]:
    """Get Cartograph Clusters For Split

     Get information about the Cartograph clusters found for a split.

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CartographClusterResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split, inference_name=inference_name)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient, inference_name: Union[Unset, str] = ""
) -> Optional[Union[CartographClusterResponse, HTTPValidationError]]:
    """Get Cartograph Clusters For Split

     Get information about the Cartograph clusters found for a split.

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CartographClusterResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id, run_id=run_id, split=split, client=client, inference_name=inference_name
        )
    ).parsed
