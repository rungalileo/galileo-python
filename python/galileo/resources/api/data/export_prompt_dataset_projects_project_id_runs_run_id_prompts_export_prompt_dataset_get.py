from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.llm_export_format import LLMExportFormat
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    run_id: str,
    *,
    export_format: Union[Unset, LLMExportFormat] = UNSET,
    include_chains: Union[Unset, bool] = True,
    columns: Union[Unset, list[str]] = UNSET,
    inputs: Union[Unset, bool] = True,
    prompts: Union[Unset, bool] = True,
    responses: Union[Unset, bool] = True,
    metrics: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_export_format: Union[Unset, str] = UNSET
    if not isinstance(export_format, Unset):
        json_export_format = export_format.value

    params["export_format"] = json_export_format

    params["include_chains"] = include_chains

    json_columns: Union[Unset, list[str]] = UNSET
    if not isinstance(columns, Unset):
        json_columns = columns

    params["columns"] = json_columns

    params["inputs"] = inputs

    params["prompts"] = prompts

    params["responses"] = responses

    params["metrics"] = metrics

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/runs/{run_id}/prompts/export_prompt_dataset",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    run_id: str,
    *,
    client: AuthenticatedClient,
    export_format: Union[Unset, LLMExportFormat] = UNSET,
    include_chains: Union[Unset, bool] = True,
    columns: Union[Unset, list[str]] = UNSET,
    inputs: Union[Unset, bool] = True,
    prompts: Union[Unset, bool] = True,
    responses: Union[Unset, bool] = True,
    metrics: Union[Unset, bool] = True,
) -> Response[Union[Any, HTTPValidationError]]:
    """Export Prompt Dataset

    Args:
        project_id (str):
        run_id (str):
        export_format (Union[Unset, LLMExportFormat]):
        include_chains (Union[Unset, bool]):  Default: True.
        columns (Union[Unset, list[str]]):
        inputs (Union[Unset, bool]):  Default: True.
        prompts (Union[Unset, bool]):  Default: True.
        responses (Union[Unset, bool]):  Default: True.
        metrics (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        export_format=export_format,
        include_chains=include_chains,
        columns=columns,
        inputs=inputs,
        prompts=prompts,
        responses=responses,
        metrics=metrics,
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    *,
    client: AuthenticatedClient,
    export_format: Union[Unset, LLMExportFormat] = UNSET,
    include_chains: Union[Unset, bool] = True,
    columns: Union[Unset, list[str]] = UNSET,
    inputs: Union[Unset, bool] = True,
    prompts: Union[Unset, bool] = True,
    responses: Union[Unset, bool] = True,
    metrics: Union[Unset, bool] = True,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Export Prompt Dataset

    Args:
        project_id (str):
        run_id (str):
        export_format (Union[Unset, LLMExportFormat]):
        include_chains (Union[Unset, bool]):  Default: True.
        columns (Union[Unset, list[str]]):
        inputs (Union[Unset, bool]):  Default: True.
        prompts (Union[Unset, bool]):  Default: True.
        responses (Union[Unset, bool]):  Default: True.
        metrics (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        client=client,
        export_format=export_format,
        include_chains=include_chains,
        columns=columns,
        inputs=inputs,
        prompts=prompts,
        responses=responses,
        metrics=metrics,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    *,
    client: AuthenticatedClient,
    export_format: Union[Unset, LLMExportFormat] = UNSET,
    include_chains: Union[Unset, bool] = True,
    columns: Union[Unset, list[str]] = UNSET,
    inputs: Union[Unset, bool] = True,
    prompts: Union[Unset, bool] = True,
    responses: Union[Unset, bool] = True,
    metrics: Union[Unset, bool] = True,
) -> Response[Union[Any, HTTPValidationError]]:
    """Export Prompt Dataset

    Args:
        project_id (str):
        run_id (str):
        export_format (Union[Unset, LLMExportFormat]):
        include_chains (Union[Unset, bool]):  Default: True.
        columns (Union[Unset, list[str]]):
        inputs (Union[Unset, bool]):  Default: True.
        prompts (Union[Unset, bool]):  Default: True.
        responses (Union[Unset, bool]):  Default: True.
        metrics (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        export_format=export_format,
        include_chains=include_chains,
        columns=columns,
        inputs=inputs,
        prompts=prompts,
        responses=responses,
        metrics=metrics,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    *,
    client: AuthenticatedClient,
    export_format: Union[Unset, LLMExportFormat] = UNSET,
    include_chains: Union[Unset, bool] = True,
    columns: Union[Unset, list[str]] = UNSET,
    inputs: Union[Unset, bool] = True,
    prompts: Union[Unset, bool] = True,
    responses: Union[Unset, bool] = True,
    metrics: Union[Unset, bool] = True,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Export Prompt Dataset

    Args:
        project_id (str):
        run_id (str):
        export_format (Union[Unset, LLMExportFormat]):
        include_chains (Union[Unset, bool]):  Default: True.
        columns (Union[Unset, list[str]]):
        inputs (Union[Unset, bool]):  Default: True.
        prompts (Union[Unset, bool]):  Default: True.
        responses (Union[Unset, bool]):  Default: True.
        metrics (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            client=client,
            export_format=export_format,
            include_chains=include_chains,
            columns=columns,
            inputs=inputs,
            prompts=prompts,
            responses=responses,
            metrics=metrics,
        )
    ).parsed
