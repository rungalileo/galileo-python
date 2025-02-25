from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_update_prompt_dataset_projects_project_id_prompt_datasets_dataset_id_put import (
    BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut,
)
from ...models.dataset_format import DatasetFormat
from ...models.http_validation_error import HTTPValidationError
from ...models.prompt_dataset_db import PromptDatasetDB
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    dataset_id: str,
    *,
    body: BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut,
    file_name: Union[None, Unset, str] = UNSET,
    num_rows: Union[None, Unset, int] = UNSET,
    format_: Union[Unset, DatasetFormat] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_file_name: Union[None, Unset, str]
    if isinstance(file_name, Unset):
        json_file_name = UNSET
    else:
        json_file_name = file_name
    params["file_name"] = json_file_name

    json_num_rows: Union[None, Unset, int]
    if isinstance(num_rows, Unset):
        json_num_rows = UNSET
    else:
        json_num_rows = num_rows
    params["num_rows"] = json_num_rows

    json_format_: Union[Unset, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/projects/{project_id}/prompt_datasets/{dataset_id}",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PromptDatasetDB]]:
    if response.status_code == 200:
        response_200 = PromptDatasetDB.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PromptDatasetDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut,
    file_name: Union[None, Unset, str] = UNSET,
    num_rows: Union[None, Unset, int] = UNSET,
    format_: Union[Unset, DatasetFormat] = UNSET,
) -> Response[Union[HTTPValidationError, PromptDatasetDB]]:
    """Update Prompt Dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_name (Union[None, Unset, str]):
        num_rows (Union[None, Unset, int]):
        format_ (Union[Unset, DatasetFormat]):
        body (BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PromptDatasetDB]]
    """

    kwargs = _get_kwargs(
        project_id=project_id, dataset_id=dataset_id, body=body, file_name=file_name, num_rows=num_rows, format_=format_
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut,
    file_name: Union[None, Unset, str] = UNSET,
    num_rows: Union[None, Unset, int] = UNSET,
    format_: Union[Unset, DatasetFormat] = UNSET,
) -> Optional[Union[HTTPValidationError, PromptDatasetDB]]:
    """Update Prompt Dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_name (Union[None, Unset, str]):
        num_rows (Union[None, Unset, int]):
        format_ (Union[Unset, DatasetFormat]):
        body (BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PromptDatasetDB]
    """

    return sync_detailed(
        project_id=project_id,
        dataset_id=dataset_id,
        client=client,
        body=body,
        file_name=file_name,
        num_rows=num_rows,
        format_=format_,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut,
    file_name: Union[None, Unset, str] = UNSET,
    num_rows: Union[None, Unset, int] = UNSET,
    format_: Union[Unset, DatasetFormat] = UNSET,
) -> Response[Union[HTTPValidationError, PromptDatasetDB]]:
    """Update Prompt Dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_name (Union[None, Unset, str]):
        num_rows (Union[None, Unset, int]):
        format_ (Union[Unset, DatasetFormat]):
        body (BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PromptDatasetDB]]
    """

    kwargs = _get_kwargs(
        project_id=project_id, dataset_id=dataset_id, body=body, file_name=file_name, num_rows=num_rows, format_=format_
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut,
    file_name: Union[None, Unset, str] = UNSET,
    num_rows: Union[None, Unset, int] = UNSET,
    format_: Union[Unset, DatasetFormat] = UNSET,
) -> Optional[Union[HTTPValidationError, PromptDatasetDB]]:
    """Update Prompt Dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_name (Union[None, Unset, str]):
        num_rows (Union[None, Unset, int]):
        format_ (Union[Unset, DatasetFormat]):
        body (BodyUpdatePromptDatasetProjectsProjectIdPromptDatasetsDatasetIdPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PromptDatasetDB]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            dataset_id=dataset_id,
            client=client,
            body=body,
            file_name=file_name,
            num_rows=num_rows,
            format_=format_,
        )
    ).parsed
