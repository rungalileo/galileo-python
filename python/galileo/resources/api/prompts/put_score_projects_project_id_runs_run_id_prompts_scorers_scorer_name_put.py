from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.put_prompt_score_request import PutPromptScoreRequest
from ...models.put_prompt_score_response import PutPromptScoreResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    body: PutPromptScoreRequest,
    monitor_batch_id: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_monitor_batch_id: Union[None, Unset, str]
    if isinstance(monitor_batch_id, Unset):
        json_monitor_batch_id = UNSET
    else:
        json_monitor_batch_id = monitor_batch_id
    params["monitor_batch_id"] = json_monitor_batch_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/projects/{project_id}/runs/{run_id}/prompts/scorers/{scorer_name}",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PutPromptScoreResponse]]:
    if response.status_code == 200:
        response_200 = PutPromptScoreResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PutPromptScoreResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    client: AuthenticatedClient,
    body: PutPromptScoreRequest,
    monitor_batch_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PutPromptScoreResponse]]:
    """Put Score

    Args:
        project_id (str):
        run_id (str):
        scorer_name (str):
        monitor_batch_id (Union[None, Unset, str]):
        body (PutPromptScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PutPromptScoreResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id, run_id=run_id, scorer_name=scorer_name, body=body, monitor_batch_id=monitor_batch_id
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    client: AuthenticatedClient,
    body: PutPromptScoreRequest,
    monitor_batch_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PutPromptScoreResponse]]:
    """Put Score

    Args:
        project_id (str):
        run_id (str):
        scorer_name (str):
        monitor_batch_id (Union[None, Unset, str]):
        body (PutPromptScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PutPromptScoreResponse]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        scorer_name=scorer_name,
        client=client,
        body=body,
        monitor_batch_id=monitor_batch_id,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    client: AuthenticatedClient,
    body: PutPromptScoreRequest,
    monitor_batch_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PutPromptScoreResponse]]:
    """Put Score

    Args:
        project_id (str):
        run_id (str):
        scorer_name (str):
        monitor_batch_id (Union[None, Unset, str]):
        body (PutPromptScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PutPromptScoreResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id, run_id=run_id, scorer_name=scorer_name, body=body, monitor_batch_id=monitor_batch_id
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    client: AuthenticatedClient,
    body: PutPromptScoreRequest,
    monitor_batch_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PutPromptScoreResponse]]:
    """Put Score

    Args:
        project_id (str):
        run_id (str):
        scorer_name (str):
        monitor_batch_id (Union[None, Unset, str]):
        body (PutPromptScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PutPromptScoreResponse]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            scorer_name=scorer_name,
            client=client,
            body=body,
            monitor_batch_id=monitor_batch_id,
        )
    ).parsed
