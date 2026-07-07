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
from ...models.http_validation_error import HTTPValidationError
from ...models.partial_extended_agent_span_record import PartialExtendedAgentSpanRecord
from ...models.partial_extended_control_span_record import PartialExtendedControlSpanRecord
from ...models.partial_extended_llm_span_record import PartialExtendedLlmSpanRecord
from ...models.partial_extended_retriever_span_record import PartialExtendedRetrieverSpanRecord
from ...models.partial_extended_session_record import PartialExtendedSessionRecord
from ...models.partial_extended_tool_span_record import PartialExtendedToolSpanRecord
from ...models.partial_extended_trace_record import PartialExtendedTraceRecord
from ...models.partial_extended_workflow_span_record import PartialExtendedWorkflowSpanRecord
from ...types import Response


def _get_kwargs(queue_id: str, record_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/annotation_queues/{queue_id}/records/{record_id}".format(queue_id=queue_id, record_id=record_id),
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[
    HTTPValidationError,
    Union[
        "PartialExtendedAgentSpanRecord",
        "PartialExtendedControlSpanRecord",
        "PartialExtendedLlmSpanRecord",
        "PartialExtendedRetrieverSpanRecord",
        "PartialExtendedSessionRecord",
        "PartialExtendedToolSpanRecord",
        "PartialExtendedTraceRecord",
        "PartialExtendedWorkflowSpanRecord",
    ],
]:
    if response.status_code == 200:

        def _parse_response_200(
            data: object,
        ) -> Union[
            "PartialExtendedAgentSpanRecord",
            "PartialExtendedControlSpanRecord",
            "PartialExtendedLlmSpanRecord",
            "PartialExtendedRetrieverSpanRecord",
            "PartialExtendedSessionRecord",
            "PartialExtendedToolSpanRecord",
            "PartialExtendedTraceRecord",
            "PartialExtendedWorkflowSpanRecord",
        ]:
            # Discriminator-aware parsing for Extended*Record types
            if isinstance(data, dict) and "type" in data:
                type_value = data.get("type")

                # Hardcoded discriminator mapping for Extended*Record types
                if type_value == "trace":
                    try:
                        from ..models.extended_trace_record import ExtendedTraceRecord

                        return ExtendedTraceRecord.from_dict(data)
                    except:  # noqa: E722
                        pass
                elif type_value == "agent":
                    try:
                        from ..models.extended_agent_span_record import ExtendedAgentSpanRecord

                        return ExtendedAgentSpanRecord.from_dict(data)
                    except:  # noqa: E722
                        pass
                elif type_value == "workflow":
                    try:
                        from ..models.extended_workflow_span_record import ExtendedWorkflowSpanRecord

                        return ExtendedWorkflowSpanRecord.from_dict(data)
                    except:  # noqa: E722
                        pass
                elif type_value == "llm":
                    try:
                        from ..models.extended_llm_span_record import ExtendedLlmSpanRecord

                        return ExtendedLlmSpanRecord.from_dict(data)
                    except:  # noqa: E722
                        pass
                elif type_value == "tool":
                    try:
                        from ..models.extended_tool_span_record import ExtendedToolSpanRecord

                        return ExtendedToolSpanRecord.from_dict(data)
                    except:  # noqa: E722
                        pass
                elif type_value == "retriever":
                    try:
                        from ..models.extended_retriever_span_record import ExtendedRetrieverSpanRecord

                        return ExtendedRetrieverSpanRecord.from_dict(data)
                    except:  # noqa: E722
                        pass
                elif type_value == "session":
                    try:
                        from ..models.extended_session_record import ExtendedSessionRecord

                        return ExtendedSessionRecord.from_dict(data)
                    except:  # noqa: E722
                        pass

            # Fallback to standard union parsing
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = PartialExtendedTraceRecord.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = PartialExtendedAgentSpanRecord.from_dict(data)

                return response_200_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_2 = PartialExtendedWorkflowSpanRecord.from_dict(data)

                return response_200_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_3 = PartialExtendedLlmSpanRecord.from_dict(data)

                return response_200_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_4 = PartialExtendedToolSpanRecord.from_dict(data)

                return response_200_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_5 = PartialExtendedRetrieverSpanRecord.from_dict(data)

                return response_200_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_6 = PartialExtendedControlSpanRecord.from_dict(data)

                return response_200_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_7 = PartialExtendedSessionRecord.from_dict(data)

                return response_200_type_7
            except:  # noqa: E722
                pass
            # If we reach here, none of the parsers succeeded
            discriminator_info = f" (type={data.get('type')})" if isinstance(data, dict) and "type" in data else ""
            raise ValueError(f"Could not parse union type for response_200{discriminator_info}")

        response_200 = _parse_response_200(response.json())

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
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "PartialExtendedAgentSpanRecord",
            "PartialExtendedControlSpanRecord",
            "PartialExtendedLlmSpanRecord",
            "PartialExtendedRetrieverSpanRecord",
            "PartialExtendedSessionRecord",
            "PartialExtendedToolSpanRecord",
            "PartialExtendedTraceRecord",
            "PartialExtendedWorkflowSpanRecord",
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
    queue_id: str, record_id: str, *, client: ApiClient
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "PartialExtendedAgentSpanRecord",
            "PartialExtendedControlSpanRecord",
            "PartialExtendedLlmSpanRecord",
            "PartialExtendedRetrieverSpanRecord",
            "PartialExtendedSessionRecord",
            "PartialExtendedToolSpanRecord",
            "PartialExtendedTraceRecord",
            "PartialExtendedWorkflowSpanRecord",
        ],
    ]
]:
    """Get Annotation Queue Record

     Get a single record in an annotation queue.

    Permission checks:
    - User must have READ permission on the annotation queue

    Args:
        queue_id (str):
        record_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['PartialExtendedAgentSpanRecord', 'PartialExtendedControlSpanRecord', 'PartialExtendedLlmSpanRecord', 'PartialExtendedRetrieverSpanRecord', 'PartialExtendedSessionRecord', 'PartialExtendedToolSpanRecord', 'PartialExtendedTraceRecord', 'PartialExtendedWorkflowSpanRecord']]]
    """

    kwargs = _get_kwargs(queue_id=queue_id, record_id=record_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    queue_id: str, record_id: str, *, client: ApiClient
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "PartialExtendedAgentSpanRecord",
            "PartialExtendedControlSpanRecord",
            "PartialExtendedLlmSpanRecord",
            "PartialExtendedRetrieverSpanRecord",
            "PartialExtendedSessionRecord",
            "PartialExtendedToolSpanRecord",
            "PartialExtendedTraceRecord",
            "PartialExtendedWorkflowSpanRecord",
        ],
    ]
]:
    """Get Annotation Queue Record

     Get a single record in an annotation queue.

    Permission checks:
    - User must have READ permission on the annotation queue

    Args:
        queue_id (str):
        record_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['PartialExtendedAgentSpanRecord', 'PartialExtendedControlSpanRecord', 'PartialExtendedLlmSpanRecord', 'PartialExtendedRetrieverSpanRecord', 'PartialExtendedSessionRecord', 'PartialExtendedToolSpanRecord', 'PartialExtendedTraceRecord', 'PartialExtendedWorkflowSpanRecord']]
    """

    return sync_detailed(queue_id=queue_id, record_id=record_id, client=client).parsed


async def asyncio_detailed(
    queue_id: str, record_id: str, *, client: ApiClient
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "PartialExtendedAgentSpanRecord",
            "PartialExtendedControlSpanRecord",
            "PartialExtendedLlmSpanRecord",
            "PartialExtendedRetrieverSpanRecord",
            "PartialExtendedSessionRecord",
            "PartialExtendedToolSpanRecord",
            "PartialExtendedTraceRecord",
            "PartialExtendedWorkflowSpanRecord",
        ],
    ]
]:
    """Get Annotation Queue Record

     Get a single record in an annotation queue.

    Permission checks:
    - User must have READ permission on the annotation queue

    Args:
        queue_id (str):
        record_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['PartialExtendedAgentSpanRecord', 'PartialExtendedControlSpanRecord', 'PartialExtendedLlmSpanRecord', 'PartialExtendedRetrieverSpanRecord', 'PartialExtendedSessionRecord', 'PartialExtendedToolSpanRecord', 'PartialExtendedTraceRecord', 'PartialExtendedWorkflowSpanRecord']]]
    """

    kwargs = _get_kwargs(queue_id=queue_id, record_id=record_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    queue_id: str, record_id: str, *, client: ApiClient
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "PartialExtendedAgentSpanRecord",
            "PartialExtendedControlSpanRecord",
            "PartialExtendedLlmSpanRecord",
            "PartialExtendedRetrieverSpanRecord",
            "PartialExtendedSessionRecord",
            "PartialExtendedToolSpanRecord",
            "PartialExtendedTraceRecord",
            "PartialExtendedWorkflowSpanRecord",
        ],
    ]
]:
    """Get Annotation Queue Record

     Get a single record in an annotation queue.

    Permission checks:
    - User must have READ permission on the annotation queue

    Args:
        queue_id (str):
        record_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['PartialExtendedAgentSpanRecord', 'PartialExtendedControlSpanRecord', 'PartialExtendedLlmSpanRecord', 'PartialExtendedRetrieverSpanRecord', 'PartialExtendedSessionRecord', 'PartialExtendedToolSpanRecord', 'PartialExtendedTraceRecord', 'PartialExtendedWorkflowSpanRecord']]
    """

    return (await asyncio_detailed(queue_id=queue_id, record_id=record_id, client=client)).parsed
