from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.validate_llm_scorer_log_record_request import ValidateLLMScorerLogRecordRequest
from ...models.validate_llm_scorer_log_record_response import ValidateLLMScorerLogRecordResponse
from ...types import Response


def _get_kwargs(*, body: ValidateLLMScorerLogRecordRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/scorers/llm/validate/log_record",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]]:
    if response.status_code == 200:
        return ValidateLLMScorerLogRecordResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: ValidateLLMScorerLogRecordRequest
) -> Response[Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]]:
    """Validate Llm Scorer Log Record

    Args:
        body (ValidateLLMScorerLogRecordRequest): Request to validate a new LLM scorer based on a
            log record.
            This is used to create a new experiment with the copied log records to store the metric
            testing results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]]
    """

    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: ValidateLLMScorerLogRecordRequest
) -> Optional[Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]]:
    """Validate Llm Scorer Log Record

    Args:
        body (ValidateLLMScorerLogRecordRequest): Request to validate a new LLM scorer based on a
            log record.
            This is used to create a new experiment with the copied log records to store the metric
            testing results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]
    """

    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: ValidateLLMScorerLogRecordRequest
) -> Response[Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]]:
    """Validate Llm Scorer Log Record

    Args:
        body (ValidateLLMScorerLogRecordRequest): Request to validate a new LLM scorer based on a
            log record.
            This is used to create a new experiment with the copied log records to store the metric
            testing results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]]
    """

    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: ValidateLLMScorerLogRecordRequest
) -> Optional[Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]]:
    """Validate Llm Scorer Log Record

    Args:
        body (ValidateLLMScorerLogRecordRequest): Request to validate a new LLM scorer based on a
            log record.
            This is used to create a new experiment with the copied log records to store the metric
            testing results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ValidateLLMScorerLogRecordResponse]
    """

    return (await asyncio_detailed(client=client, body=body)).parsed
