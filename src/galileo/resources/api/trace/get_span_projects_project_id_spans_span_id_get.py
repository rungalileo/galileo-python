from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.extended_agent_span_record_with_children import ExtendedAgentSpanRecordWithChildren
from ...models.extended_llm_span_record import ExtendedLlmSpanRecord
from ...models.extended_retriever_span_record_with_children import ExtendedRetrieverSpanRecordWithChildren
from ...models.extended_tool_span_record_with_children import ExtendedToolSpanRecordWithChildren
from ...models.extended_workflow_span_record_with_children import ExtendedWorkflowSpanRecordWithChildren
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, span_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/spans/{span_id}",
    }

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "ExtendedAgentSpanRecordWithChildren",
            "ExtendedLlmSpanRecord",
            "ExtendedRetrieverSpanRecordWithChildren",
            "ExtendedToolSpanRecordWithChildren",
            "ExtendedWorkflowSpanRecordWithChildren",
        ],
    ]
]:
    if response.status_code == 200:

        def _parse_response_200(
            data: object,
        ) -> Union[
            "ExtendedAgentSpanRecordWithChildren",
            "ExtendedLlmSpanRecord",
            "ExtendedRetrieverSpanRecordWithChildren",
            "ExtendedToolSpanRecordWithChildren",
            "ExtendedWorkflowSpanRecordWithChildren",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedAgentSpanRecordWithChildren.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedWorkflowSpanRecordWithChildren.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedLlmSpanRecord.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExtendedToolSpanRecordWithChildren.from_dict(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            return ExtendedRetrieverSpanRecordWithChildren.from_dict(data)

        return _parse_response_200(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "ExtendedAgentSpanRecordWithChildren",
            "ExtendedLlmSpanRecord",
            "ExtendedRetrieverSpanRecordWithChildren",
            "ExtendedToolSpanRecordWithChildren",
            "ExtendedWorkflowSpanRecordWithChildren",
        ],
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, span_id: str, *, client: ApiClient
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "ExtendedAgentSpanRecordWithChildren",
            "ExtendedLlmSpanRecord",
            "ExtendedRetrieverSpanRecordWithChildren",
            "ExtendedToolSpanRecordWithChildren",
            "ExtendedWorkflowSpanRecordWithChildren",
        ],
    ]
]:
    """Get Span.

    Args:
        project_id (str):
        span_id (str):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, Union['ExtendedAgentSpanRecordWithChildren', 'ExtendedLlmSpanRecord', 'ExtendedRetrieverSpanRecordWithChildren', 'ExtendedToolSpanRecordWithChildren', 'ExtendedWorkflowSpanRecordWithChildren']]]
    """
    kwargs = _get_kwargs(project_id=project_id, span_id=span_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, span_id: str, *, client: ApiClient
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "ExtendedAgentSpanRecordWithChildren",
            "ExtendedLlmSpanRecord",
            "ExtendedRetrieverSpanRecordWithChildren",
            "ExtendedToolSpanRecordWithChildren",
            "ExtendedWorkflowSpanRecordWithChildren",
        ],
    ]
]:
    """Get Span.

    Args:
        project_id (str):
        span_id (str):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, Union['ExtendedAgentSpanRecordWithChildren', 'ExtendedLlmSpanRecord', 'ExtendedRetrieverSpanRecordWithChildren', 'ExtendedToolSpanRecordWithChildren', 'ExtendedWorkflowSpanRecordWithChildren']]
    """
    return sync_detailed(project_id=project_id, span_id=span_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, span_id: str, *, client: ApiClient
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "ExtendedAgentSpanRecordWithChildren",
            "ExtendedLlmSpanRecord",
            "ExtendedRetrieverSpanRecordWithChildren",
            "ExtendedToolSpanRecordWithChildren",
            "ExtendedWorkflowSpanRecordWithChildren",
        ],
    ]
]:
    """Get Span.

    Args:
        project_id (str):
        span_id (str):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, Union['ExtendedAgentSpanRecordWithChildren', 'ExtendedLlmSpanRecord', 'ExtendedRetrieverSpanRecordWithChildren', 'ExtendedToolSpanRecordWithChildren', 'ExtendedWorkflowSpanRecordWithChildren']]]
    """
    kwargs = _get_kwargs(project_id=project_id, span_id=span_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, span_id: str, *, client: ApiClient
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "ExtendedAgentSpanRecordWithChildren",
            "ExtendedLlmSpanRecord",
            "ExtendedRetrieverSpanRecordWithChildren",
            "ExtendedToolSpanRecordWithChildren",
            "ExtendedWorkflowSpanRecordWithChildren",
        ],
    ]
]:
    """Get Span.

    Args:
        project_id (str):
        span_id (str):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, Union['ExtendedAgentSpanRecordWithChildren', 'ExtendedLlmSpanRecord', 'ExtendedRetrieverSpanRecordWithChildren', 'ExtendedToolSpanRecordWithChildren', 'ExtendedWorkflowSpanRecordWithChildren']]
    """
    return (await asyncio_detailed(project_id=project_id, span_id=span_id, client=client)).parsed
