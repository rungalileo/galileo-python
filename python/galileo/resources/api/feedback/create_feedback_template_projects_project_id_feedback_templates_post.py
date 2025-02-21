from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feedback_template_create import FeedbackTemplateCreate
from ...models.feedback_template_db import FeedbackTemplateDB
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, *, body: FeedbackTemplateCreate) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/projects/{project_id}/feedback/templates"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[FeedbackTemplateDB, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = FeedbackTemplateDB.from_dict(response.json())

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
) -> Response[Union[FeedbackTemplateDB, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: AuthenticatedClient, body: FeedbackTemplateCreate
) -> Response[Union[FeedbackTemplateDB, HTTPValidationError]]:
    """Create Feedback Template

    Args:
        project_id (str):
        body (FeedbackTemplateCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedbackTemplateDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: AuthenticatedClient, body: FeedbackTemplateCreate
) -> Optional[Union[FeedbackTemplateDB, HTTPValidationError]]:
    """Create Feedback Template

    Args:
        project_id (str):
        body (FeedbackTemplateCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedbackTemplateDB, HTTPValidationError]
    """

    return sync_detailed(project_id=project_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, *, client: AuthenticatedClient, body: FeedbackTemplateCreate
) -> Response[Union[FeedbackTemplateDB, HTTPValidationError]]:
    """Create Feedback Template

    Args:
        project_id (str):
        body (FeedbackTemplateCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedbackTemplateDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: AuthenticatedClient, body: FeedbackTemplateCreate
) -> Optional[Union[FeedbackTemplateDB, HTTPValidationError]]:
    """Create Feedback Template

    Args:
        project_id (str):
        body (FeedbackTemplateCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedbackTemplateDB, HTTPValidationError]
    """

    return (await asyncio_detailed(project_id=project_id, client=client, body=body)).parsed
