from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feature_columns_response import FeatureColumnsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, run_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/runs/{run_id}/features/columns"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[FeatureColumnsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = FeatureColumnsResponse.from_dict(response.json())

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
) -> Response[Union[FeatureColumnsResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient
) -> Response[Union[FeatureColumnsResponse, HTTPValidationError]]:
    """List Feature Columns

     Lists the names of the features for a given project_id/run_id.

    This endpoint is for tabular data only.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeatureColumnsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, *, client: AuthenticatedClient
) -> Optional[Union[FeatureColumnsResponse, HTTPValidationError]]:
    """List Feature Columns

     Lists the names of the features for a given project_id/run_id.

    This endpoint is for tabular data only.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeatureColumnsResponse, HTTPValidationError]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient
) -> Response[Union[FeatureColumnsResponse, HTTPValidationError]]:
    """List Feature Columns

     Lists the names of the features for a given project_id/run_id.

    This endpoint is for tabular data only.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeatureColumnsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, *, client: AuthenticatedClient
) -> Optional[Union[FeatureColumnsResponse, HTTPValidationError]]:
    """List Feature Columns

     Lists the names of the features for a given project_id/run_id.

    This endpoint is for tabular data only.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeatureColumnsResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client)).parsed
