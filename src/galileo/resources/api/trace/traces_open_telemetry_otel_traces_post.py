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
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    content_type: str | Unset = UNSET,
    content_encoding: None | str | Unset = UNSET,
    project: None | str | Unset = UNSET,
    projectid: None | str | Unset = UNSET,
    logstreamid: None | str | Unset = UNSET,
    logstream: None | str | Unset = UNSET,
    experimentid: None | str | Unset = UNSET,
    experiment: None | str | Unset = UNSET,
    sessionid: str | Unset = "00000000-0000-0000-0000-000000000000",
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(content_type, Unset):
        headers["content-type"] = content_type

    if not isinstance(content_encoding, Unset):
        headers["content-encoding"] = content_encoding

    if not isinstance(project, Unset):
        headers["project"] = project

    if not isinstance(projectid, Unset):
        headers["projectid"] = projectid

    if not isinstance(logstreamid, Unset):
        headers["logstreamid"] = logstreamid

    if not isinstance(logstream, Unset):
        headers["logstream"] = logstream

    if not isinstance(experimentid, Unset):
        headers["experimentid"] = experimentid

    if not isinstance(experiment, Unset):
        headers["experiment"] = experiment

    if not isinstance(sessionid, Unset):
        headers["sessionid"] = sessionid

    _kwargs: dict[str, Any] = {"method": RequestMethod.POST, "return_raw_response": True, "path": "/otel/traces"}

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Any | HTTPValidationError:
    if response.status_code == 200:
        response_200 = response.json()
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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: ApiClient,
    content_type: str | Unset = UNSET,
    content_encoding: None | str | Unset = UNSET,
    project: None | str | Unset = UNSET,
    projectid: None | str | Unset = UNSET,
    logstreamid: None | str | Unset = UNSET,
    logstream: None | str | Unset = UNSET,
    experimentid: None | str | Unset = UNSET,
    experiment: None | str | Unset = UNSET,
    sessionid: str | Unset = "00000000-0000-0000-0000-000000000000",
) -> Response[Any | HTTPValidationError]:
    """Traces Open Telemetry

    Args:
        content_type (str | Unset):
        content_encoding (None | str | Unset):
        project (None | str | Unset):
        projectid (None | str | Unset):
        logstreamid (None | str | Unset):
        logstream (None | str | Unset):
        experimentid (None | str | Unset):
        experiment (None | str | Unset):
        sessionid (str | Unset):  Default: '00000000-0000-0000-0000-000000000000'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        content_type=content_type,
        content_encoding=content_encoding,
        project=project,
        projectid=projectid,
        logstreamid=logstreamid,
        logstream=logstream,
        experimentid=experimentid,
        experiment=experiment,
        sessionid=sessionid,
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: ApiClient,
    content_type: str | Unset = UNSET,
    content_encoding: None | str | Unset = UNSET,
    project: None | str | Unset = UNSET,
    projectid: None | str | Unset = UNSET,
    logstreamid: None | str | Unset = UNSET,
    logstream: None | str | Unset = UNSET,
    experimentid: None | str | Unset = UNSET,
    experiment: None | str | Unset = UNSET,
    sessionid: str | Unset = "00000000-0000-0000-0000-000000000000",
) -> Optional[Any | HTTPValidationError]:
    """Traces Open Telemetry

    Args:
        content_type (str | Unset):
        content_encoding (None | str | Unset):
        project (None | str | Unset):
        projectid (None | str | Unset):
        logstreamid (None | str | Unset):
        logstream (None | str | Unset):
        experimentid (None | str | Unset):
        experiment (None | str | Unset):
        sessionid (str | Unset):  Default: '00000000-0000-0000-0000-000000000000'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        content_type=content_type,
        content_encoding=content_encoding,
        project=project,
        projectid=projectid,
        logstreamid=logstreamid,
        logstream=logstream,
        experimentid=experimentid,
        experiment=experiment,
        sessionid=sessionid,
    ).parsed


async def asyncio_detailed(
    *,
    client: ApiClient,
    content_type: str | Unset = UNSET,
    content_encoding: None | str | Unset = UNSET,
    project: None | str | Unset = UNSET,
    projectid: None | str | Unset = UNSET,
    logstreamid: None | str | Unset = UNSET,
    logstream: None | str | Unset = UNSET,
    experimentid: None | str | Unset = UNSET,
    experiment: None | str | Unset = UNSET,
    sessionid: str | Unset = "00000000-0000-0000-0000-000000000000",
) -> Response[Any | HTTPValidationError]:
    """Traces Open Telemetry

    Args:
        content_type (str | Unset):
        content_encoding (None | str | Unset):
        project (None | str | Unset):
        projectid (None | str | Unset):
        logstreamid (None | str | Unset):
        logstream (None | str | Unset):
        experimentid (None | str | Unset):
        experiment (None | str | Unset):
        sessionid (str | Unset):  Default: '00000000-0000-0000-0000-000000000000'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        content_type=content_type,
        content_encoding=content_encoding,
        project=project,
        projectid=projectid,
        logstreamid=logstreamid,
        logstream=logstream,
        experimentid=experimentid,
        experiment=experiment,
        sessionid=sessionid,
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: ApiClient,
    content_type: str | Unset = UNSET,
    content_encoding: None | str | Unset = UNSET,
    project: None | str | Unset = UNSET,
    projectid: None | str | Unset = UNSET,
    logstreamid: None | str | Unset = UNSET,
    logstream: None | str | Unset = UNSET,
    experimentid: None | str | Unset = UNSET,
    experiment: None | str | Unset = UNSET,
    sessionid: str | Unset = "00000000-0000-0000-0000-000000000000",
) -> Optional[Any | HTTPValidationError]:
    """Traces Open Telemetry

    Args:
        content_type (str | Unset):
        content_encoding (None | str | Unset):
        project (None | str | Unset):
        projectid (None | str | Unset):
        logstreamid (None | str | Unset):
        logstream (None | str | Unset):
        experimentid (None | str | Unset):
        experiment (None | str | Unset):
        sessionid (str | Unset):  Default: '00000000-0000-0000-0000-000000000000'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            content_type=content_type,
            content_encoding=content_encoding,
            project=project,
            projectid=projectid,
            logstreamid=logstreamid,
            logstream=logstream,
            experimentid=experimentid,
            experiment=experiment,
            sessionid=sessionid,
        )
    ).parsed
