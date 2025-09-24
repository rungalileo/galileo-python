from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient
from ...types import Response, UNSET
from ... import errors

from ...models.extended_session_record_with_children import ExtendedSessionRecordWithChildren
from ...models.http_validation_error import HTTPValidationError
from typing import cast



def _get_kwargs(
    project_id: str,
    session_id: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    

    

    

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/projects/{project_id}/sessions/{session_id}".format(project_id=project_id,session_id=session_id,),
    }


    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[Union[ExtendedSessionRecordWithChildren, HTTPValidationError]]:
    if response.status_code == :
        response_200 = ExtendedSessionRecordWithChildren.from_dict(response.json())



        return response_200
    if response.status_code == :
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[ExtendedSessionRecordWithChildren, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    session_id: str,
    *,
    client: ApiClient,

) -> Response[Union[ExtendedSessionRecordWithChildren, HTTPValidationError]]:
    """ Get Session

    Args:
        project_id (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExtendedSessionRecordWithChildren, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
session_id=session_id,

    )

    response = client.request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    session_id: str,
    *,
    client: ApiClient,

) -> Optional[Union[ExtendedSessionRecordWithChildren, HTTPValidationError]]:
    """ Get Session

    Args:
        project_id (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExtendedSessionRecordWithChildren, HTTPValidationError]
     """


    return sync_detailed(
        project_id=project_id,
session_id=session_id,
client=client,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    session_id: str,
    *,
    client: ApiClient,

) -> Response[Union[ExtendedSessionRecordWithChildren, HTTPValidationError]]:
    """ Get Session

    Args:
        project_id (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExtendedSessionRecordWithChildren, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
session_id=session_id,

    )

    response = await client.arequest(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    session_id: str,
    *,
    client: ApiClient,

) -> Optional[Union[ExtendedSessionRecordWithChildren, HTTPValidationError]]:
    """ Get Session

    Args:
        project_id (str):
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExtendedSessionRecordWithChildren, HTTPValidationError]
     """


    return (await asyncio_detailed(
        project_id=project_id,
session_id=session_id,
client=client,

    )).parsed
