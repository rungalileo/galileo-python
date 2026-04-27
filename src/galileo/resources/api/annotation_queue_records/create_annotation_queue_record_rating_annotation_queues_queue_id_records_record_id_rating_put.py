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
from ...models.annotation_rating_create import AnnotationRatingCreate
from ...models.annotation_rating_db import AnnotationRatingDB
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    queue_id: str, record_id: str, *, body: AnnotationRatingCreate, annotation_template_id: str
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["annotation_template_id"] = annotation_template_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PUT,
        "return_raw_response": True,
        "path": "/annotation_queues/{queue_id}/records/{record_id}/rating".format(
            queue_id=queue_id, record_id=record_id
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> AnnotationRatingDB | HTTPValidationError:
    if response.status_code == 200:
        response_200 = AnnotationRatingDB.from_dict(response.json())

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
) -> Response[AnnotationRatingDB | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    queue_id: str, record_id: str, *, client: ApiClient, body: AnnotationRatingCreate, annotation_template_id: str
) -> Response[AnnotationRatingDB | HTTPValidationError]:
    """Create Annotation Queue Record Rating

     Create an annotation rating for a record in an annotation queue.

    This endpoint is project-unaware and takes the template_id in the query params.

    Args:
        queue_id (str):
        record_id (str):
        annotation_template_id (str):
        body (AnnotationRatingCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationRatingDB | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        queue_id=queue_id, record_id=record_id, body=body, annotation_template_id=annotation_template_id
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    queue_id: str, record_id: str, *, client: ApiClient, body: AnnotationRatingCreate, annotation_template_id: str
) -> Optional[AnnotationRatingDB | HTTPValidationError]:
    """Create Annotation Queue Record Rating

     Create an annotation rating for a record in an annotation queue.

    This endpoint is project-unaware and takes the template_id in the query params.

    Args:
        queue_id (str):
        record_id (str):
        annotation_template_id (str):
        body (AnnotationRatingCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotationRatingDB | HTTPValidationError
    """

    return sync_detailed(
        queue_id=queue_id, record_id=record_id, client=client, body=body, annotation_template_id=annotation_template_id
    ).parsed


async def asyncio_detailed(
    queue_id: str, record_id: str, *, client: ApiClient, body: AnnotationRatingCreate, annotation_template_id: str
) -> Response[AnnotationRatingDB | HTTPValidationError]:
    """Create Annotation Queue Record Rating

     Create an annotation rating for a record in an annotation queue.

    This endpoint is project-unaware and takes the template_id in the query params.

    Args:
        queue_id (str):
        record_id (str):
        annotation_template_id (str):
        body (AnnotationRatingCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationRatingDB | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        queue_id=queue_id, record_id=record_id, body=body, annotation_template_id=annotation_template_id
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    queue_id: str, record_id: str, *, client: ApiClient, body: AnnotationRatingCreate, annotation_template_id: str
) -> Optional[AnnotationRatingDB | HTTPValidationError]:
    """Create Annotation Queue Record Rating

     Create an annotation rating for a record in an annotation queue.

    This endpoint is project-unaware and takes the template_id in the query params.

    Args:
        queue_id (str):
        record_id (str):
        annotation_template_id (str):
        body (AnnotationRatingCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotationRatingDB | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            queue_id=queue_id,
            record_id=record_id,
            client=client,
            body=body,
            annotation_template_id=annotation_template_id,
        )
    ).parsed
