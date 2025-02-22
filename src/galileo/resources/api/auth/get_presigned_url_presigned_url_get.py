from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_presigned_url_response import GetPresignedUrlResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.method import Method
from ...types import UNSET, Response


def _get_kwargs(*, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["api_url"] = api_url

    json_method = method.value
    params["method"] = json_method

    params["bucket_name"] = bucket_name

    params["object_name"] = object_name

    params["project_id"] = project_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": "/presigned_url", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetPresignedUrlResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetPresignedUrlResponse.from_dict(response.json())

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
) -> Response[Union[GetPresignedUrlResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str
) -> Response[Union[GetPresignedUrlResponse, HTTPValidationError]]:
    """Get Presigned Url

    Args:
        api_url (str):
        method (Method):
        bucket_name (str):
        object_name (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPresignedUrlResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        api_url=api_url, method=method, bucket_name=bucket_name, object_name=object_name, project_id=project_id
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str
) -> Optional[Union[GetPresignedUrlResponse, HTTPValidationError]]:
    """Get Presigned Url

    Args:
        api_url (str):
        method (Method):
        bucket_name (str):
        object_name (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPresignedUrlResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        api_url=api_url,
        method=method,
        bucket_name=bucket_name,
        object_name=object_name,
        project_id=project_id,
    ).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str
) -> Response[Union[GetPresignedUrlResponse, HTTPValidationError]]:
    """Get Presigned Url

    Args:
        api_url (str):
        method (Method):
        bucket_name (str):
        object_name (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPresignedUrlResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        api_url=api_url, method=method, bucket_name=bucket_name, object_name=object_name, project_id=project_id
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, api_url: str, method: Method, bucket_name: str, object_name: str, project_id: str
) -> Optional[Union[GetPresignedUrlResponse, HTTPValidationError]]:
    """Get Presigned Url

    Args:
        api_url (str):
        method (Method):
        bucket_name (str):
        object_name (str):
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPresignedUrlResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            api_url=api_url,
            method=method,
            bucket_name=bucket_name,
            object_name=object_name,
            project_id=project_id,
        )
    ).parsed
