from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post_response_get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post import (
    GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost,
)
from ...models.get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post_row_ids import (
    GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    body: GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/runs/prompts/rows/columnar",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost,
        HTTPValidationError,
    ]
]:
    if response.status_code == 200:
        response_200 = GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost.from_dict(
            response.json()
        )

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
) -> Response[
    Union[
        GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost,
        HTTPValidationError,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[
    Union[
        GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost,
        HTTPValidationError,
    ]
]:
    """Get Multi Run Samples For Row Ids

     Given run_ids with their corresponding row ids, retrieve the samples for those row_ids.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body, starting_token=starting_token, limit=limit)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[
    Union[
        GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost,
        HTTPValidationError,
    ]
]:
    """Get Multi Run Samples For Row Ids

     Given run_ids with their corresponding row ids, retrieve the samples for those row_ids.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id, client=client, body=body, starting_token=starting_token, limit=limit
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[
    Union[
        GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost,
        HTTPValidationError,
    ]
]:
    """Get Multi Run Samples For Row Ids

     Given run_ids with their corresponding row ids, retrieve the samples for those row_ids.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body, starting_token=starting_token, limit=limit)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[
    Union[
        GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost,
        HTTPValidationError,
    ]
]:
    """Get Multi Run Samples For Row Ids

     Given run_ids with their corresponding row ids, retrieve the samples for those row_ids.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id, client=client, body=body, starting_token=starting_token, limit=limit
        )
    ).parsed
