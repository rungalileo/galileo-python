from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.inference_run_results import InferenceRunResults
from ...models.split import Split
from ...models.split_run_results import SplitRunResults
from ...models.summary_request import SummaryRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, run_id: str, split: Split, *, body: SummaryRequest, inference_name: Union[Unset, str] = ""
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["inference_name"] = inference_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/insights/summary",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["InferenceRunResults", "SplitRunResults"]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["InferenceRunResults", "SplitRunResults"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_root_model_union_inference_run_results_split_run_results_type_0 = (
                    InferenceRunResults.from_dict(data)
                )

                return componentsschemas_root_model_union_inference_run_results_split_run_results_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_root_model_union_inference_run_results_split_run_results_type_1 = (
                SplitRunResults.from_dict(data)
            )

            return componentsschemas_root_model_union_inference_run_results_split_run_results_type_1

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, Union["InferenceRunResults", "SplitRunResults"]]]:
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
    body: SummaryRequest,
    inference_name: Union[Unset, str] = "",
) -> Response[Union[HTTPValidationError, Union["InferenceRunResults", "SplitRunResults"]]]:
    r"""Get Summary Statistics

     Populates the core components of the Galileo Console.

    Calculate summary statistics, data rows, hard/easy thresholds, DEP distribution for
     the cohort, and applies any filters requested.

    Args:
        project_id
        run_id
        split
        current_user (User, optional): The current user making the HTTP request.
            Defaults to Depends(authentication_service.current_user).
        inference_name (bool, default \"\"): Optional inference name. Required if split
            is inference
        summary_request (SummaryRequest, optional): See SummaryRequest.

    Returns:
        SplitRunResults

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (SummaryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['InferenceRunResults', 'SplitRunResults']]]
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
    body: SummaryRequest,
    inference_name: Union[Unset, str] = "",
) -> Optional[Union[HTTPValidationError, Union["InferenceRunResults", "SplitRunResults"]]]:
    r"""Get Summary Statistics

     Populates the core components of the Galileo Console.

    Calculate summary statistics, data rows, hard/easy thresholds, DEP distribution for
     the cohort, and applies any filters requested.

    Args:
        project_id
        run_id
        split
        current_user (User, optional): The current user making the HTTP request.
            Defaults to Depends(authentication_service.current_user).
        inference_name (bool, default \"\"): Optional inference name. Required if split
            is inference
        summary_request (SummaryRequest, optional): See SummaryRequest.

    Returns:
        SplitRunResults

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (SummaryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['InferenceRunResults', 'SplitRunResults']]
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
    body: SummaryRequest,
    inference_name: Union[Unset, str] = "",
) -> Response[Union[HTTPValidationError, Union["InferenceRunResults", "SplitRunResults"]]]:
    r"""Get Summary Statistics

     Populates the core components of the Galileo Console.

    Calculate summary statistics, data rows, hard/easy thresholds, DEP distribution for
     the cohort, and applies any filters requested.

    Args:
        project_id
        run_id
        split
        current_user (User, optional): The current user making the HTTP request.
            Defaults to Depends(authentication_service.current_user).
        inference_name (bool, default \"\"): Optional inference name. Required if split
            is inference
        summary_request (SummaryRequest, optional): See SummaryRequest.

    Returns:
        SplitRunResults

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (SummaryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['InferenceRunResults', 'SplitRunResults']]]
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
    body: SummaryRequest,
    inference_name: Union[Unset, str] = "",
) -> Optional[Union[HTTPValidationError, Union["InferenceRunResults", "SplitRunResults"]]]:
    r"""Get Summary Statistics

     Populates the core components of the Galileo Console.

    Calculate summary statistics, data rows, hard/easy thresholds, DEP distribution for
     the cohort, and applies any filters requested.

    Args:
        project_id
        run_id
        split
        current_user (User, optional): The current user making the HTTP request.
            Defaults to Depends(authentication_service.current_user).
        inference_name (bool, default \"\"): Optional inference name. Required if split
            is inference
        summary_request (SummaryRequest, optional): See SummaryRequest.

    Returns:
        SplitRunResults

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        body (SummaryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['InferenceRunResults', 'SplitRunResults']]
    """

    return (
        await asyncio_detailed(
            project_id=project_id, run_id=run_id, split=split, client=client, body=body, inference_name=inference_name
        )
    ).parsed
