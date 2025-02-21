from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_get_response import EditGetResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_inference_name: Union[None, Unset, str]
    if isinstance(inference_name, Unset):
        json_inference_name = UNSET
    else:
        json_inference_name = inference_name
    params["inference_name"] = json_inference_name

    params["include_exported"] = include_exported

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/edits",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["EditGetResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EditGetResponse.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["EditGetResponse"]]]:
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
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, list["EditGetResponse"]]]:
    """Get Run Edits

     Gets all edits in a project/run/split.

    :param project_id: project_id :param run_id: run_id :param split: split :param include_exported:
    Whether to also
    query exported (past) edits. Default True. If True, return will include historical edits that have
    already been
    exported

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[None, Unset, str]):
        include_exported (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['EditGetResponse']]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        split=split,
        inference_name=inference_name,
        include_exported=include_exported,
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, list["EditGetResponse"]]]:
    """Get Run Edits

     Gets all edits in a project/run/split.

    :param project_id: project_id :param run_id: run_id :param split: split :param include_exported:
    Whether to also
    query exported (past) edits. Default True. If True, return will include historical edits that have
    already been
    exported

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[None, Unset, str]):
        include_exported (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['EditGetResponse']]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        split=split,
        client=client,
        inference_name=inference_name,
        include_exported=include_exported,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, list["EditGetResponse"]]]:
    """Get Run Edits

     Gets all edits in a project/run/split.

    :param project_id: project_id :param run_id: run_id :param split: split :param include_exported:
    Whether to also
    query exported (past) edits. Default True. If True, return will include historical edits that have
    already been
    exported

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[None, Unset, str]):
        include_exported (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['EditGetResponse']]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        split=split,
        inference_name=inference_name,
        include_exported=include_exported,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, list["EditGetResponse"]]]:
    """Get Run Edits

     Gets all edits in a project/run/split.

    :param project_id: project_id :param run_id: run_id :param split: split :param include_exported:
    Whether to also
    query exported (past) edits. Default True. If True, return will include historical edits that have
    already been
    exported

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[None, Unset, str]):
        include_exported (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['EditGetResponse']]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            split=split,
            client=client,
            inference_name=inference_name,
            include_exported=include_exported,
        )
    ).parsed
