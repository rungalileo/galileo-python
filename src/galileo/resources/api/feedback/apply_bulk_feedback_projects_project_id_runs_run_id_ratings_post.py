from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_feedback_rating_status import BulkFeedbackRatingStatus
from ...models.bulk_feedback_request import BulkFeedbackRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, run_id: str, *, body: BulkFeedbackRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/projects/{project_id}/runs/{run_id}/ratings"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["BulkFeedbackRatingStatus"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = BulkFeedbackRatingStatus.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["BulkFeedbackRatingStatus"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, body: BulkFeedbackRequest
) -> Response[Union[HTTPValidationError, list["BulkFeedbackRatingStatus"]]]:
    """Apply Bulk Feedback

     Record multiple feedback ratings

    Args:
        project_id (str):
        run_id (str):
        body (BulkFeedbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['BulkFeedbackRatingStatus']]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, *, client: AuthenticatedClient, body: BulkFeedbackRequest
) -> Optional[Union[HTTPValidationError, list["BulkFeedbackRatingStatus"]]]:
    """Apply Bulk Feedback

     Record multiple feedback ratings

    Args:
        project_id (str):
        run_id (str):
        body (BulkFeedbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['BulkFeedbackRatingStatus']]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, body: BulkFeedbackRequest
) -> Response[Union[HTTPValidationError, list["BulkFeedbackRatingStatus"]]]:
    """Apply Bulk Feedback

     Record multiple feedback ratings

    Args:
        project_id (str):
        run_id (str):
        body (BulkFeedbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['BulkFeedbackRatingStatus']]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, *, client: AuthenticatedClient, body: BulkFeedbackRequest
) -> Optional[Union[HTTPValidationError, list["BulkFeedbackRatingStatus"]]]:
    """Apply Bulk Feedback

     Record multiple feedback ratings

    Args:
        project_id (str):
        run_id (str):
        body (BulkFeedbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['BulkFeedbackRatingStatus']]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client, body=body)).parsed
