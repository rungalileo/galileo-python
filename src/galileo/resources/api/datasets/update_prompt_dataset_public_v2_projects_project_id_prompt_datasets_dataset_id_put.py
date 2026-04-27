from http import HTTPStatus
from typing import Any, Optional

import httpx

from galileo.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.body_update_prompt_dataset_public_v2_projects_project_id_prompt_datasets_dataset_id_put import (
    BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut,
)
from ...models.dataset_format import DatasetFormat
from ...models.http_validation_error import HTTPValidationError
from ...models.prompt_dataset_db import PromptDatasetDB
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    dataset_id: str,
    *,
    body: BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset,
    file_name: None | str | Unset = UNSET,
    num_rows: int | None | Unset = UNSET,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_file_name: None | str | Unset
    if isinstance(file_name, Unset):
        json_file_name = UNSET
    else:
        json_file_name = file_name
    params["file_name"] = json_file_name

    json_num_rows: int | None | Unset
    if isinstance(num_rows, Unset):
        json_num_rows = UNSET
    else:
        json_num_rows = num_rows
    params["num_rows"] = json_num_rows

    json_format_: str | Unset = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params["hidden"] = hidden

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PUT,
        "return_raw_response": True,
        "path": "/public/v2/projects/{project_id}/prompt_datasets/{dataset_id}".format(
            project_id=project_id, dataset_id=dataset_id
        ),
        "params": params,
    }

    if not isinstance(body, Unset):
        _kwargs["files"] = body.to_multipart()

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | PromptDatasetDB:
    if response.status_code == 200:
        response_200 = PromptDatasetDB.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    # Handle common HTTP errors with actionable messages
    if response.status_code == 400:
        raise BadRequestError(response.status_code, response.content)
    if response.status_code == 401:
        raise AuthenticationError(response.status_code, response.content)
    if response.status_code == 403:
        raise ForbiddenError(response.status_code, response.content)
    if response.status_code == 404:
        raise NotFoundError(response.status_code, response.content)
    if response.status_code == 409:
        raise ConflictError(response.status_code, response.content)
    if response.status_code == 429:
        raise RateLimitError(response.status_code, response.content)
    if response.status_code >= 500:
        raise ServerError(response.status_code, response.content)
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[HTTPValidationError | PromptDatasetDB]:
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
    client: ApiClient,
    body: BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset,
    file_name: None | str | Unset = UNSET,
    num_rows: int | None | Unset = UNSET,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> Response[HTTPValidationError | PromptDatasetDB]:
    """Update Prompt Dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_name (None | str | Unset):
        num_rows (int | None | Unset):
        format_ (DatasetFormat | Unset):
        hidden (bool | Unset):  Default: False.
        body (BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PromptDatasetDB]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
        body=body,
        file_name=file_name,
        num_rows=num_rows,
        format_=format_,
        hidden=hidden,
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    dataset_id: str,
    *,
    client: ApiClient,
    body: BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset,
    file_name: None | str | Unset = UNSET,
    num_rows: int | None | Unset = UNSET,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> Optional[HTTPValidationError | PromptDatasetDB]:
    """Update Prompt Dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_name (None | str | Unset):
        num_rows (int | None | Unset):
        format_ (DatasetFormat | Unset):
        hidden (bool | Unset):  Default: False.
        body (BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PromptDatasetDB
    """

    return sync_detailed(
        project_id=project_id,
        dataset_id=dataset_id,
        client=client,
        body=body,
        file_name=file_name,
        num_rows=num_rows,
        format_=format_,
        hidden=hidden,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    dataset_id: str,
    *,
    client: ApiClient,
    body: BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset,
    file_name: None | str | Unset = UNSET,
    num_rows: int | None | Unset = UNSET,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> Response[HTTPValidationError | PromptDatasetDB]:
    """Update Prompt Dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_name (None | str | Unset):
        num_rows (int | None | Unset):
        format_ (DatasetFormat | Unset):
        hidden (bool | Unset):  Default: False.
        body (BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PromptDatasetDB]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        dataset_id=dataset_id,
        body=body,
        file_name=file_name,
        num_rows=num_rows,
        format_=format_,
        hidden=hidden,
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    dataset_id: str,
    *,
    client: ApiClient,
    body: BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset,
    file_name: None | str | Unset = UNSET,
    num_rows: int | None | Unset = UNSET,
    format_: DatasetFormat | Unset = UNSET,
    hidden: bool | Unset = False,
) -> Optional[HTTPValidationError | PromptDatasetDB]:
    """Update Prompt Dataset

    Args:
        project_id (str):
        dataset_id (str):
        file_name (None | str | Unset):
        num_rows (int | None | Unset):
        format_ (DatasetFormat | Unset):
        hidden (bool | Unset):  Default: False.
        body (BodyUpdatePromptDatasetPublicV2ProjectsProjectIdPromptDatasetsDatasetIdPut | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PromptDatasetDB
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
            hidden=hidden,
        )
    ).parsed
