from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_review_db import EditReviewDB
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(edit_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "post", "url": f"/edits/{edit_id}/review"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[EditReviewDB, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = EditReviewDB.from_dict(response.json())

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
) -> Response[Union[EditReviewDB, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(edit_id: str, *, client: AuthenticatedClient) -> Response[Union[EditReviewDB, HTTPValidationError]]:
    """Add Review For Edit

     Add a review for an edit.

    Must have access to the run with which the edit exists in. Users CAN review their own edits (as per
    ticket
    instructions)

    Args:
        edit_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditReviewDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(edit_id=edit_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(edit_id: str, *, client: AuthenticatedClient) -> Optional[Union[EditReviewDB, HTTPValidationError]]:
    """Add Review For Edit

     Add a review for an edit.

    Must have access to the run with which the edit exists in. Users CAN review their own edits (as per
    ticket
    instructions)

    Args:
        edit_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditReviewDB, HTTPValidationError]
    """

    return sync_detailed(edit_id=edit_id, client=client).parsed


async def asyncio_detailed(
    edit_id: str, *, client: AuthenticatedClient
) -> Response[Union[EditReviewDB, HTTPValidationError]]:
    """Add Review For Edit

     Add a review for an edit.

    Must have access to the run with which the edit exists in. Users CAN review their own edits (as per
    ticket
    instructions)

    Args:
        edit_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditReviewDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(edit_id=edit_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(edit_id: str, *, client: AuthenticatedClient) -> Optional[Union[EditReviewDB, HTTPValidationError]]:
    """Add Review For Edit

     Add a review for an edit.

    Must have access to the run with which the edit exists in. Users CAN review their own edits (as per
    ticket
    instructions)

    Args:
        edit_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditReviewDB, HTTPValidationError]
    """

    return (await asyncio_detailed(edit_id=edit_id, client=client)).parsed
