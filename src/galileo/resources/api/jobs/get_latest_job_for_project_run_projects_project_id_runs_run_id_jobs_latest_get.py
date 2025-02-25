from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.job_db import JobDB
from ...types import Response


def _get_kwargs(project_id: str, run_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/runs/{run_id}/jobs/latest"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["JobDB", None]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["JobDB", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = JobDB.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            return cast(Union["JobDB", None], data)

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
) -> Response[Union[HTTPValidationError, Union["JobDB", None]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, Union["JobDB", None]]]:
    """Get Latest Job For Project Run

     Returns the most recently updated job for a run.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['JobDB', None]]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, Union["JobDB", None]]]:
    """Get Latest Job For Project Run

     Returns the most recently updated job for a run.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['JobDB', None]]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, Union["JobDB", None]]]:
    """Get Latest Job For Project Run

     Returns the most recently updated job for a run.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['JobDB', None]]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, Union["JobDB", None]]]:
    """Get Latest Job For Project Run

     Returns the most recently updated job for a run.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['JobDB', None]]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client)).parsed
