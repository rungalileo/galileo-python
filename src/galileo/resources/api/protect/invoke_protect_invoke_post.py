from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.invoke_response import InvokeResponse
from ...models.protect_request import ProtectRequest
from ...models.protect_response import ProtectResponse
from ...types import Response


def _get_kwargs(*, body: ProtectRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": RequestMethod.POST, "return_raw_response": True, "path": "/protect/invoke"}

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["InvokeResponse", "ProtectResponse"]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["InvokeResponse", "ProtectResponse"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = ProtectResponse.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = InvokeResponse.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, Union["InvokeResponse", "ProtectResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: ProtectRequest
) -> Response[Union[HTTPValidationError, Union["InvokeResponse", "ProtectResponse"]]]:
    """Invoke

    Args:
        body (ProtectRequest): Protect request schema with custom OpenAPI title.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['InvokeResponse', 'ProtectResponse']]]
    """

    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: ProtectRequest
) -> Optional[Union[HTTPValidationError, Union["InvokeResponse", "ProtectResponse"]]]:
    """Invoke

    Args:
        body (ProtectRequest): Protect request schema with custom OpenAPI title.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['InvokeResponse', 'ProtectResponse']]
    """

    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: ProtectRequest
) -> Response[Union[HTTPValidationError, Union["InvokeResponse", "ProtectResponse"]]]:
    """Invoke

    Args:
        body (ProtectRequest): Protect request schema with custom OpenAPI title.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['InvokeResponse', 'ProtectResponse']]]
    """

    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: ProtectRequest
) -> Optional[Union[HTTPValidationError, Union["InvokeResponse", "ProtectResponse"]]]:
    """Invoke

    Args:
        body (ProtectRequest): Protect request schema with custom OpenAPI title.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['InvokeResponse', 'ProtectResponse']]
    """

    return (await asyncio_detailed(client=client, body=body)).parsed
