from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.create_llm_scorer_autogen_request import CreateLLMScorerAutogenRequest
from ...models.generation_response import GenerationResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(*, body: CreateLLMScorerAutogenRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/scorers/llm/autogen",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[GenerationResponse, HTTPValidationError]]:
    if response.status_code == 200:
        return GenerationResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[GenerationResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: CreateLLMScorerAutogenRequest
) -> Response[Union[GenerationResponse, HTTPValidationError]]:
    """Autogen Llm Scorer.

     Autogenerate an LLM scorer configuration.

    Returns a Celery task ID that can be used to poll for the autogeneration results.

    Args:
        body (CreateLLMScorerAutogenRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[GenerationResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: CreateLLMScorerAutogenRequest
) -> Optional[Union[GenerationResponse, HTTPValidationError]]:
    """Autogen Llm Scorer.

     Autogenerate an LLM scorer configuration.

    Returns a Celery task ID that can be used to poll for the autogeneration results.

    Args:
        body (CreateLLMScorerAutogenRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[GenerationResponse, HTTPValidationError]
    """
    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: CreateLLMScorerAutogenRequest
) -> Response[Union[GenerationResponse, HTTPValidationError]]:
    """Autogen Llm Scorer.

     Autogenerate an LLM scorer configuration.

    Returns a Celery task ID that can be used to poll for the autogeneration results.

    Args:
        body (CreateLLMScorerAutogenRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[GenerationResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: CreateLLMScorerAutogenRequest
) -> Optional[Union[GenerationResponse, HTTPValidationError]]:
    """Autogen Llm Scorer.

     Autogenerate an LLM scorer configuration.

    Returns a Celery task ID that can be used to poll for the autogeneration results.

    Args:
        body (CreateLLMScorerAutogenRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[GenerationResponse, HTTPValidationError]
    """
    return (await asyncio_detailed(client=client, body=body)).parsed
