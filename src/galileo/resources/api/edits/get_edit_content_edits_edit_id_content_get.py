from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_content import EditContent
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    edit_id: str,
    *,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page_num"] = page_num

    json_meta_cols: Union[None, Unset, list[str]]
    if isinstance(meta_cols, Unset):
        json_meta_cols = UNSET
    elif isinstance(meta_cols, list):
        json_meta_cols = meta_cols

    else:
        json_meta_cols = meta_cols
    params["meta_cols"] = json_meta_cols

    json_text_pat: Union[None, Unset, str]
    if isinstance(text_pat, Unset):
        json_text_pat = UNSET
    else:
        json_text_pat = text_pat
    params["text_pat"] = json_text_pat

    json_regex: Union[None, Unset, bool]
    if isinstance(regex, Unset):
        json_regex = UNSET
    else:
        json_regex = regex
    params["regex"] = json_regex

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/edits/{edit_id}/content", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[EditContent, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = EditContent.from_dict(response.json())

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
) -> Response[Union[EditContent, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    edit_id: str,
    *,
    client: AuthenticatedClient,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> Response[Union[EditContent, HTTPValidationError]]:
    """Get Edit Content

     Gets the data for an edit, including the text, predicted label and true label.

    Args:
        edit_id (str):
        page_num (Union[Unset, int]):  Default: 0.
        meta_cols (Union[None, Unset, list[str]]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditContent, HTTPValidationError]]
    """

    kwargs = _get_kwargs(edit_id=edit_id, page_num=page_num, meta_cols=meta_cols, text_pat=text_pat, regex=regex)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    edit_id: str,
    *,
    client: AuthenticatedClient,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[EditContent, HTTPValidationError]]:
    """Get Edit Content

     Gets the data for an edit, including the text, predicted label and true label.

    Args:
        edit_id (str):
        page_num (Union[Unset, int]):  Default: 0.
        meta_cols (Union[None, Unset, list[str]]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditContent, HTTPValidationError]
    """

    return sync_detailed(
        edit_id=edit_id, client=client, page_num=page_num, meta_cols=meta_cols, text_pat=text_pat, regex=regex
    ).parsed


async def asyncio_detailed(
    edit_id: str,
    *,
    client: AuthenticatedClient,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> Response[Union[EditContent, HTTPValidationError]]:
    """Get Edit Content

     Gets the data for an edit, including the text, predicted label and true label.

    Args:
        edit_id (str):
        page_num (Union[Unset, int]):  Default: 0.
        meta_cols (Union[None, Unset, list[str]]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditContent, HTTPValidationError]]
    """

    kwargs = _get_kwargs(edit_id=edit_id, page_num=page_num, meta_cols=meta_cols, text_pat=text_pat, regex=regex)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    edit_id: str,
    *,
    client: AuthenticatedClient,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[EditContent, HTTPValidationError]]:
    """Get Edit Content

     Gets the data for an edit, including the text, predicted label and true label.

    Args:
        edit_id (str):
        page_num (Union[Unset, int]):  Default: 0.
        meta_cols (Union[None, Unset, list[str]]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditContent, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            edit_id=edit_id, client=client, page_num=page_num, meta_cols=meta_cols, text_pat=text_pat, regex=regex
        )
    ).parsed
