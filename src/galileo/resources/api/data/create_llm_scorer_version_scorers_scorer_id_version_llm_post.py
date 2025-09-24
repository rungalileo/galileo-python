from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient
from ...types import Response, UNSET
from ... import errors

from ...models.base_scorer_version_response import BaseScorerVersionResponse
from ...models.create_llm_scorer_version_request import CreateLLMScorerVersionRequest
from ...models.http_validation_error import HTTPValidationError
from typing import cast



def _get_kwargs(
    scorer_id: str,
    *,
    body: CreateLLMScorerVersionRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    

    

    

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/scorers/{scorer_id}/version/llm".format(scorer_id=scorer_id,),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[Union[BaseScorerVersionResponse, HTTPValidationError]]:
    if response.status_code == :
        response_200 = BaseScorerVersionResponse.from_dict(response.json())



        return response_200
    if response.status_code == :
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[BaseScorerVersionResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scorer_id: str,
    *,
    client: ApiClient,
    body: CreateLLMScorerVersionRequest,

) -> Response[Union[BaseScorerVersionResponse, HTTPValidationError]]:
    """ Create Llm Scorer Version

    Args:
        scorer_id (str):
        body (CreateLLMScorerVersionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BaseScorerVersionResponse, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        scorer_id=scorer_id,
body=body,

    )

    response = client.request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    scorer_id: str,
    *,
    client: ApiClient,
    body: CreateLLMScorerVersionRequest,

) -> Optional[Union[BaseScorerVersionResponse, HTTPValidationError]]:
    """ Create Llm Scorer Version

    Args:
        scorer_id (str):
        body (CreateLLMScorerVersionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BaseScorerVersionResponse, HTTPValidationError]
     """


    return sync_detailed(
        scorer_id=scorer_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    scorer_id: str,
    *,
    client: ApiClient,
    body: CreateLLMScorerVersionRequest,

) -> Response[Union[BaseScorerVersionResponse, HTTPValidationError]]:
    """ Create Llm Scorer Version

    Args:
        scorer_id (str):
        body (CreateLLMScorerVersionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BaseScorerVersionResponse, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        scorer_id=scorer_id,
body=body,

    )

    response = await client.arequest(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    scorer_id: str,
    *,
    client: ApiClient,
    body: CreateLLMScorerVersionRequest,

) -> Optional[Union[BaseScorerVersionResponse, HTTPValidationError]]:
    """ Create Llm Scorer Version

    Args:
        scorer_id (str):
        body (CreateLLMScorerVersionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BaseScorerVersionResponse, HTTPValidationError]
     """


    return (await asyncio_detailed(
        scorer_id=scorer_id,
client=client,
body=body,

    )).parsed
