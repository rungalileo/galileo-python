from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cbo_cluster_request import CBOClusterRequest
from ...models.cbo_cluster_response import CBOClusterResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, run_id: str, split: Split, *, body: CBOClusterRequest, inference_name: Union[Unset, str] = ""
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["inference_name"] = inference_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/insights/cbo_clusters",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CBOClusterResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = CBOClusterResponse.from_dict(response.json())

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
) -> Response[Union[CBOClusterResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: CBOClusterRequest,
    inference_name: Union[Unset, str] = "",
) -> Response[Union[CBOClusterResponse, HTTPValidationError]]:
    """Get Cbo Clusters For Split

     Returns the list of available CBO (class boundary overlap) clusters for the.

    dataframe given some (or no) filters.

    The clusters are returned as a list of CBOCluster in order of num_samples descending

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (CBOClusterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CBOClusterResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split, body=body, inference_name=inference_name)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: CBOClusterRequest,
    inference_name: Union[Unset, str] = "",
) -> Optional[Union[CBOClusterResponse, HTTPValidationError]]:
    """Get Cbo Clusters For Split

     Returns the list of available CBO (class boundary overlap) clusters for the.

    dataframe given some (or no) filters.

    The clusters are returned as a list of CBOCluster in order of num_samples descending

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (CBOClusterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CBOClusterResponse, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id, run_id=run_id, split=split, client=client, body=body, inference_name=inference_name
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: CBOClusterRequest,
    inference_name: Union[Unset, str] = "",
) -> Response[Union[CBOClusterResponse, HTTPValidationError]]:
    """Get Cbo Clusters For Split

     Returns the list of available CBO (class boundary overlap) clusters for the.

    dataframe given some (or no) filters.

    The clusters are returned as a list of CBOCluster in order of num_samples descending

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (CBOClusterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CBOClusterResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split, body=body, inference_name=inference_name)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: CBOClusterRequest,
    inference_name: Union[Unset, str] = "",
) -> Optional[Union[CBOClusterResponse, HTTPValidationError]]:
    """Get Cbo Clusters For Split

     Returns the list of available CBO (class boundary overlap) clusters for the.

    dataframe given some (or no) filters.

    The clusters are returned as a list of CBOCluster in order of num_samples descending

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (CBOClusterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CBOClusterResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id, run_id=run_id, split=split, client=client, body=body, inference_name=inference_name
        )
    ).parsed
