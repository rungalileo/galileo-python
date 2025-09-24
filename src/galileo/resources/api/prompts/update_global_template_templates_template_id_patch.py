from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient
from ...types import Response, UNSET
from ... import errors

from ...models.base_prompt_template_response import BasePromptTemplateResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.update_prompt_template_request import UpdatePromptTemplateRequest
from typing import cast



def _get_kwargs(
    template_id: str,
    *,
    body: UpdatePromptTemplateRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    

    

    

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PATCH,
        "return_raw_response": True,
        "path": "/templates/{template_id}".format(template_id=template_id,),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    if response.status_code == :
        response_200 = BasePromptTemplateResponse.from_dict(response.json())



        return response_200
    if response.status_code == :
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id: str,
    *,
    client: ApiClient,
    body: UpdatePromptTemplateRequest,

) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """ Update Global Template

     Update a global prompt template.

    Parameters
    ----------
    update_template_request : UpdatePromptTemplateRequest
        Request containing the fields to update.
    template : PromptTemplate
        Prompt template to update.
    principal : Principal
        Principal object.
    ctx : Context
        Request context including authentication information.

    Returns
    -------
    BasePromptTemplateResponse
        Updated prompt template.

    Args:
        template_id (str):
        body (UpdatePromptTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateResponse, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        template_id=template_id,
body=body,

    )

    response = client.request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    template_id: str,
    *,
    client: ApiClient,
    body: UpdatePromptTemplateRequest,

) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """ Update Global Template

     Update a global prompt template.

    Parameters
    ----------
    update_template_request : UpdatePromptTemplateRequest
        Request containing the fields to update.
    template : PromptTemplate
        Prompt template to update.
    principal : Principal
        Principal object.
    ctx : Context
        Request context including authentication information.

    Returns
    -------
    BasePromptTemplateResponse
        Updated prompt template.

    Args:
        template_id (str):
        body (UpdatePromptTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateResponse, HTTPValidationError]
     """


    return sync_detailed(
        template_id=template_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    template_id: str,
    *,
    client: ApiClient,
    body: UpdatePromptTemplateRequest,

) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """ Update Global Template

     Update a global prompt template.

    Parameters
    ----------
    update_template_request : UpdatePromptTemplateRequest
        Request containing the fields to update.
    template : PromptTemplate
        Prompt template to update.
    principal : Principal
        Principal object.
    ctx : Context
        Request context including authentication information.

    Returns
    -------
    BasePromptTemplateResponse
        Updated prompt template.

    Args:
        template_id (str):
        body (UpdatePromptTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateResponse, HTTPValidationError]]
     """


    kwargs = _get_kwargs(
        template_id=template_id,
body=body,

    )

    response = await client.arequest(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    template_id: str,
    *,
    client: ApiClient,
    body: UpdatePromptTemplateRequest,

) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """ Update Global Template

     Update a global prompt template.

    Parameters
    ----------
    update_template_request : UpdatePromptTemplateRequest
        Request containing the fields to update.
    template : PromptTemplate
        Prompt template to update.
    principal : Principal
        Principal object.
    ctx : Context
        Request context including authentication information.

    Returns
    -------
    BasePromptTemplateResponse
        Updated prompt template.

    Args:
        template_id (str):
        body (UpdatePromptTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateResponse, HTTPValidationError]
     """


    return (await asyncio_detailed(
        template_id=template_id,
client=client,
body=body,

    )).parsed
