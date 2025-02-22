from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.upload_model import UploadModel
from ...models.upload_model_response import UploadModelResponse
from ...types import Response


def _get_kwargs(project_id: str, run_id: str, *, body: UploadModel) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/projects/{project_id}/runs/{run_id}/model"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, UploadModelResponse]]:
    if response.status_code == 200:
        response_200 = UploadModelResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UploadModelResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, body: UploadModel
) -> Response[Union[HTTPValidationError, UploadModelResponse]]:
    """Upload Model

     Uploads a model to the object store and creates a model record in the database :param project_id:
    project id
    :param run_id: run id :param validation_request: model upload request.

    Args:
        project_id (str):
        run_id (str):
        body (UploadModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UploadModelResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, *, client: AuthenticatedClient, body: UploadModel
) -> Optional[Union[HTTPValidationError, UploadModelResponse]]:
    """Upload Model

     Uploads a model to the object store and creates a model record in the database :param project_id:
    project id
    :param run_id: run id :param validation_request: model upload request.

    Args:
        project_id (str):
        run_id (str):
        body (UploadModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UploadModelResponse]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, body: UploadModel
) -> Response[Union[HTTPValidationError, UploadModelResponse]]:
    """Upload Model

     Uploads a model to the object store and creates a model record in the database :param project_id:
    project id
    :param run_id: run id :param validation_request: model upload request.

    Args:
        project_id (str):
        run_id (str):
        body (UploadModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UploadModelResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, *, client: AuthenticatedClient, body: UploadModel
) -> Optional[Union[HTTPValidationError, UploadModelResponse]]:
    """Upload Model

     Uploads a model to the object store and creates a model record in the database :param project_id:
    project id
    :param run_id: run id :param validation_request: model upload request.

    Args:
        project_id (str):
        run_id (str):
        body (UploadModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UploadModelResponse]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client, body=body)).parsed
