from http import HTTPStatus
from typing import Any, Optional, Union

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
from ...models.generated_scorer_validation_response import GeneratedScorerValidationResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.manual_llm_validate_scorers_llm_validate_post_body import ManualLlmValidateScorersLlmValidatePostBody
from ...types import Response


def _get_kwargs(*, body: ManualLlmValidateScorersLlmValidatePostBody) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/scorers/llm/validate",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[GeneratedScorerValidationResponse, HTTPValidationError]:
    if response.status_code == 200:
        return GeneratedScorerValidationResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

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
) -> Response[Union[GeneratedScorerValidationResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: ManualLlmValidateScorersLlmValidatePostBody
) -> Response[Union[GeneratedScorerValidationResponse, HTTPValidationError]]:
    """Manual Llm Validate.

    Args:
        body (ManualLlmValidateScorersLlmValidatePostBody):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[GeneratedScorerValidationResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: ManualLlmValidateScorersLlmValidatePostBody
) -> Optional[Union[GeneratedScorerValidationResponse, HTTPValidationError]]:
    """Manual Llm Validate.

    Args:
        body (ManualLlmValidateScorersLlmValidatePostBody):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[GeneratedScorerValidationResponse, HTTPValidationError]
    """
    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: ManualLlmValidateScorersLlmValidatePostBody
) -> Response[Union[GeneratedScorerValidationResponse, HTTPValidationError]]:
    """Manual Llm Validate.

    Args:
        body (ManualLlmValidateScorersLlmValidatePostBody):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[GeneratedScorerValidationResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: ManualLlmValidateScorersLlmValidatePostBody
) -> Optional[Union[GeneratedScorerValidationResponse, HTTPValidationError]]:
    """Manual Llm Validate.

    Args:
        body (ManualLlmValidateScorersLlmValidatePostBody):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[GeneratedScorerValidationResponse, HTTPValidationError]
    """
    return (await asyncio_detailed(client=client, body=body)).parsed
