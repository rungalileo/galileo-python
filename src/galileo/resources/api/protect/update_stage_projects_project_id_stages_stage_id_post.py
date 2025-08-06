from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.rulesets_mixin import RulesetsMixin
from ...models.stage_db import StageDB
from ...types import Response


def _get_kwargs(project_id: str, stage_id: str, *, body: RulesetsMixin) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/stages/{stage_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[Union[HTTPValidationError, StageDB]]:
    if response.status_code == 200:
        response_200 = StageDB.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[HTTPValidationError, StageDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, stage_id: str, *, client: ApiClient, body: RulesetsMixin
) -> Response[Union[HTTPValidationError, StageDB]]:
    """Update Stage

    Args:
        project_id (str):
        stage_id (str):
        body (RulesetsMixin):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StageDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, stage_id=stage_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, stage_id: str, *, client: ApiClient, body: RulesetsMixin
) -> Optional[Union[HTTPValidationError, StageDB]]:
    """Update Stage

    Args:
        project_id (str):
        stage_id (str):
        body (RulesetsMixin):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StageDB]
    """

    return sync_detailed(project_id=project_id, stage_id=stage_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, stage_id: str, *, client: ApiClient, body: RulesetsMixin
) -> Response[Union[HTTPValidationError, StageDB]]:
    """Update Stage

    Args:
        project_id (str):
        stage_id (str):
        body (RulesetsMixin):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StageDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, stage_id=stage_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, stage_id: str, *, client: ApiClient, body: RulesetsMixin
) -> Optional[Union[HTTPValidationError, StageDB]]:
    """Update Stage

    Args:
        project_id (str):
        stage_id (str):
        body (RulesetsMixin):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StageDB]
    """

    return (await asyncio_detailed(project_id=project_id, stage_id=stage_id, client=client, body=body)).parsed
