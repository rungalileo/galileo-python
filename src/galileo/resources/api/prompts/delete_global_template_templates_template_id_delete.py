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
from ...models.delete_prompt_response import DeletePromptResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(template_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.DELETE,
        "return_raw_response": True,
        "path": "/templates/{template_id}".format(template_id=template_id),
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> DeletePromptResponse | HTTPValidationError:
    if response.status_code == 200:
        response_200 = DeletePromptResponse.from_dict(response.json())

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


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[DeletePromptResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(template_id: str, *, client: ApiClient) -> Response[DeletePromptResponse | HTTPValidationError]:
    """Delete Global Template

     Delete a global prompt template given a template ID.

    Parameters
    ----------
    template_id : UUID4
        Prompt template id.
    ctx : Context
        Request context including authentication information

    Returns
    -------
    DeletePromptResponse
        Message indicating the prompt template was deleted.

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeletePromptResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(template_id=template_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(template_id: str, *, client: ApiClient) -> Optional[DeletePromptResponse | HTTPValidationError]:
    """Delete Global Template

     Delete a global prompt template given a template ID.

    Parameters
    ----------
    template_id : UUID4
        Prompt template id.
    ctx : Context
        Request context including authentication information

    Returns
    -------
    DeletePromptResponse
        Message indicating the prompt template was deleted.

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeletePromptResponse | HTTPValidationError
    """

    return sync_detailed(template_id=template_id, client=client).parsed


async def asyncio_detailed(
    template_id: str, *, client: ApiClient
) -> Response[DeletePromptResponse | HTTPValidationError]:
    """Delete Global Template

     Delete a global prompt template given a template ID.

    Parameters
    ----------
    template_id : UUID4
        Prompt template id.
    ctx : Context
        Request context including authentication information

    Returns
    -------
    DeletePromptResponse
        Message indicating the prompt template was deleted.

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeletePromptResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(template_id=template_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(template_id: str, *, client: ApiClient) -> Optional[DeletePromptResponse | HTTPValidationError]:
    """Delete Global Template

     Delete a global prompt template given a template ID.

    Parameters
    ----------
    template_id : UUID4
        Prompt template id.
    ctx : Context
        Request context including authentication information

    Returns
    -------
    DeletePromptResponse
        Message indicating the prompt template was deleted.

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeletePromptResponse | HTTPValidationError
    """

    return (await asyncio_detailed(template_id=template_id, client=client)).parsed
