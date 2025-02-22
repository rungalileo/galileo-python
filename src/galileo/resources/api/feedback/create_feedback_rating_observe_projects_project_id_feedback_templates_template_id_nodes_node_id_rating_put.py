from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feedback_rating_create import FeedbackRatingCreate
from ...models.feedback_rating_db import FeedbackRatingDB
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, template_id: str, node_id: str, *, body: FeedbackRatingCreate) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/projects/{project_id}/feedback/templates/{template_id}/nodes/{node_id}/rating",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[FeedbackRatingDB, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = FeedbackRatingDB.from_dict(response.json())

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
) -> Response[Union[FeedbackRatingDB, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, template_id: str, node_id: str, *, client: AuthenticatedClient, body: FeedbackRatingCreate
) -> Response[Union[FeedbackRatingDB, HTTPValidationError]]:
    """Create Feedback Rating Observe

     Record a feedack rating for a specific sample in a run. For prompt chains, the index must be the
    root node.

    Args:
        project_id (str):
        template_id (str):
        node_id (str):
        body (FeedbackRatingCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedbackRatingDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, template_id=template_id, node_id=node_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, template_id: str, node_id: str, *, client: AuthenticatedClient, body: FeedbackRatingCreate
) -> Optional[Union[FeedbackRatingDB, HTTPValidationError]]:
    """Create Feedback Rating Observe

     Record a feedack rating for a specific sample in a run. For prompt chains, the index must be the
    root node.

    Args:
        project_id (str):
        template_id (str):
        node_id (str):
        body (FeedbackRatingCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedbackRatingDB, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id, template_id=template_id, node_id=node_id, client=client, body=body
    ).parsed


async def asyncio_detailed(
    project_id: str, template_id: str, node_id: str, *, client: AuthenticatedClient, body: FeedbackRatingCreate
) -> Response[Union[FeedbackRatingDB, HTTPValidationError]]:
    """Create Feedback Rating Observe

     Record a feedack rating for a specific sample in a run. For prompt chains, the index must be the
    root node.

    Args:
        project_id (str):
        template_id (str):
        node_id (str):
        body (FeedbackRatingCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedbackRatingDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, template_id=template_id, node_id=node_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, template_id: str, node_id: str, *, client: AuthenticatedClient, body: FeedbackRatingCreate
) -> Optional[Union[FeedbackRatingDB, HTTPValidationError]]:
    """Create Feedback Rating Observe

     Record a feedack rating for a specific sample in a run. For prompt chains, the index must be the
    root node.

    Args:
        project_id (str):
        template_id (str):
        node_id (str):
        body (FeedbackRatingCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedbackRatingDB, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id, template_id=template_id, node_id=node_id, client=client, body=body
        )
    ).parsed
