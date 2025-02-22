from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...models.x_ray_card_db import XRayCardDB
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    inference_name: Union[Unset, str] = "",
    include_dismissed: Union[Unset, bool] = False,
    map_threshold: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["inference_name"] = inference_name

    params["include_dismissed"] = include_dismissed

    json_map_threshold: Union[None, Unset, str]
    if isinstance(map_threshold, Unset):
        json_map_threshold = UNSET
    else:
        json_map_threshold = map_threshold
    params["map_threshold"] = json_map_threshold

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/insights/alerts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["XRayCardDB"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = XRayCardDB.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, list["XRayCardDB"]]]:
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
    inference_name: Union[Unset, str] = "",
    include_dismissed: Union[Unset, bool] = False,
    map_threshold: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, list["XRayCardDB"]]]:
    """Get Alerts For Run

     Gets alerts for project/run/split.

    Optionally gets dismissed cards as well

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        include_dismissed (Union[Unset, bool]):  Default: False.
        map_threshold (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['XRayCardDB']]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        split=split,
        inference_name=inference_name,
        include_dismissed=include_dismissed,
        map_threshold=map_threshold,
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[Unset, str] = "",
    include_dismissed: Union[Unset, bool] = False,
    map_threshold: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, list["XRayCardDB"]]]:
    """Get Alerts For Run

     Gets alerts for project/run/split.

    Optionally gets dismissed cards as well

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        include_dismissed (Union[Unset, bool]):  Default: False.
        map_threshold (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['XRayCardDB']]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        split=split,
        client=client,
        inference_name=inference_name,
        include_dismissed=include_dismissed,
        map_threshold=map_threshold,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[Unset, str] = "",
    include_dismissed: Union[Unset, bool] = False,
    map_threshold: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, list["XRayCardDB"]]]:
    """Get Alerts For Run

     Gets alerts for project/run/split.

    Optionally gets dismissed cards as well

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        include_dismissed (Union[Unset, bool]):  Default: False.
        map_threshold (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['XRayCardDB']]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        split=split,
        inference_name=inference_name,
        include_dismissed=include_dismissed,
        map_threshold=map_threshold,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[Unset, str] = "",
    include_dismissed: Union[Unset, bool] = False,
    map_threshold: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, list["XRayCardDB"]]]:
    """Get Alerts For Run

     Gets alerts for project/run/split.

    Optionally gets dismissed cards as well

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        include_dismissed (Union[Unset, bool]):  Default: False.
        map_threshold (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['XRayCardDB']]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            split=split,
            client=client,
            inference_name=inference_name,
            include_dismissed=include_dismissed,
            map_threshold=map_threshold,
        )
    ).parsed
