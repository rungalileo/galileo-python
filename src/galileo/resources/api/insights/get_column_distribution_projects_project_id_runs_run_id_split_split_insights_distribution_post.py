from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.distribution import Distribution
from ...models.distribution_request import DistributionRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, run_id: str, split: Split, *, body: DistributionRequest, inference_name: Union[Unset, str] = ""
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["inference_name"] = inference_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/insights/distribution",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Distribution, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = Distribution.from_dict(response.json())

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
) -> Response[Union[Distribution, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: DistributionRequest,
    inference_name: Union[Unset, str] = "",
) -> Response[Union[Distribution, HTTPValidationError]]:
    r"""Get Column Distribution

     Calculates density distribution / histogram for a numeric column.

    Args:
        project_id
        run_id
        split
        inference_name (bool, default \"\"): Optional inference name. Required if split
            is inference
        current_user (User, optional): The current user making the HTTP request.
            Defaults to Depends(authentication_service.current_user).

        distribution_request (DistributionRequest):
        In request body:
        col: Required. The column to calculate distribution on
        nbins: Number of bins for the distribution. Default 20
        limit_min: Minimum value for the limit of the dist. Default to min of column
        limit_max: Maximum value for the limit of the dist. Default to min of column
        Inherits from ContentRequest.
            - Optional filters for the request

    Returns:
        Distribution

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (DistributionRequest): A distribution histogram for a run/filter for a particular
            numerical column.

            bins are boundaries for the x axis and counts are the y axis. bins will have 1 more value
            than counts because the
            count at index i is for the range [bin[i], bin[i+1]), with the lower boundary inclusive
            and the upper boundary
            exclusive

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Distribution, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split, body=body, inference_name=inference_name)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: DistributionRequest,
    inference_name: Union[Unset, str] = "",
) -> Optional[Union[Distribution, HTTPValidationError]]:
    r"""Get Column Distribution

     Calculates density distribution / histogram for a numeric column.

    Args:
        project_id
        run_id
        split
        inference_name (bool, default \"\"): Optional inference name. Required if split
            is inference
        current_user (User, optional): The current user making the HTTP request.
            Defaults to Depends(authentication_service.current_user).

        distribution_request (DistributionRequest):
        In request body:
        col: Required. The column to calculate distribution on
        nbins: Number of bins for the distribution. Default 20
        limit_min: Minimum value for the limit of the dist. Default to min of column
        limit_max: Maximum value for the limit of the dist. Default to min of column
        Inherits from ContentRequest.
            - Optional filters for the request

    Returns:
        Distribution

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (DistributionRequest): A distribution histogram for a run/filter for a particular
            numerical column.

            bins are boundaries for the x axis and counts are the y axis. bins will have 1 more value
            than counts because the
            count at index i is for the range [bin[i], bin[i+1]), with the lower boundary inclusive
            and the upper boundary
            exclusive

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Distribution, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id, run_id=run_id, split=split, client=client, body=body, inference_name=inference_name
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: DistributionRequest,
    inference_name: Union[Unset, str] = "",
) -> Response[Union[Distribution, HTTPValidationError]]:
    r"""Get Column Distribution

     Calculates density distribution / histogram for a numeric column.

    Args:
        project_id
        run_id
        split
        inference_name (bool, default \"\"): Optional inference name. Required if split
            is inference
        current_user (User, optional): The current user making the HTTP request.
            Defaults to Depends(authentication_service.current_user).

        distribution_request (DistributionRequest):
        In request body:
        col: Required. The column to calculate distribution on
        nbins: Number of bins for the distribution. Default 20
        limit_min: Minimum value for the limit of the dist. Default to min of column
        limit_max: Maximum value for the limit of the dist. Default to min of column
        Inherits from ContentRequest.
            - Optional filters for the request

    Returns:
        Distribution

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (DistributionRequest): A distribution histogram for a run/filter for a particular
            numerical column.

            bins are boundaries for the x axis and counts are the y axis. bins will have 1 more value
            than counts because the
            count at index i is for the range [bin[i], bin[i+1]), with the lower boundary inclusive
            and the upper boundary
            exclusive

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Distribution, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split, body=body, inference_name=inference_name)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: DistributionRequest,
    inference_name: Union[Unset, str] = "",
) -> Optional[Union[Distribution, HTTPValidationError]]:
    r"""Get Column Distribution

     Calculates density distribution / histogram for a numeric column.

    Args:
        project_id
        run_id
        split
        inference_name (bool, default \"\"): Optional inference name. Required if split
            is inference
        current_user (User, optional): The current user making the HTTP request.
            Defaults to Depends(authentication_service.current_user).

        distribution_request (DistributionRequest):
        In request body:
        col: Required. The column to calculate distribution on
        nbins: Number of bins for the distribution. Default 20
        limit_min: Minimum value for the limit of the dist. Default to min of column
        limit_max: Maximum value for the limit of the dist. Default to min of column
        Inherits from ContentRequest.
            - Optional filters for the request

    Returns:
        Distribution

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (DistributionRequest): A distribution histogram for a run/filter for a particular
            numerical column.

            bins are boundaries for the x axis and counts are the y axis. bins will have 1 more value
            than counts because the
            count at index i is for the range [bin[i], bin[i+1]), with the lower boundary inclusive
            and the upper boundary
            exclusive

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Distribution, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id, run_id=run_id, split=split, client=client, body=body, inference_name=inference_name
        )
    ).parsed
