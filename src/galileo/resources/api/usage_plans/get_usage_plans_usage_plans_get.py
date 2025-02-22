from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_usage_plans_usage_plans_get_response_get_usage_plans_usage_plans_get import (
    GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet,
)
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": "/usage_plans"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet]:
    if response.status_code == 200:
        response_200 = GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient
) -> Response[GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet]:
    """Get Usage Plans

     Get the static usage plans for the supported subscription plans.

    Returns:
        dict[UsagePlanName, UsagePlan]: A dictionary mapping subscription plan types
            to their corresponding usage plans.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: AuthenticatedClient) -> Optional[GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet]:
    """Get Usage Plans

     Get the static usage plans for the supported subscription plans.

    Returns:
        dict[UsagePlanName, UsagePlan]: A dictionary mapping subscription plan types
            to their corresponding usage plans.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet
    """

    return sync_detailed(client=client).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient
) -> Response[GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet]:
    """Get Usage Plans

     Get the static usage plans for the supported subscription plans.

    Returns:
        dict[UsagePlanName, UsagePlan]: A dictionary mapping subscription plan types
            to their corresponding usage plans.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient
) -> Optional[GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet]:
    """Get Usage Plans

     Get the static usage plans for the supported subscription plans.

    Returns:
        dict[UsagePlanName, UsagePlan]: A dictionary mapping subscription plan types
            to their corresponding usage plans.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet
    """

    return (await asyncio_detailed(client=client)).parsed
