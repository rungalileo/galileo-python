from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_content import EditContent
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_inference_name: Union[None, Unset, str]
    if isinstance(inference_name, Unset):
        json_inference_name = UNSET
    else:
        json_inference_name = inference_name
    params["inference_name"] = json_inference_name

    params["include_exported"] = include_exported

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

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/edits/content",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["EditContent"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EditContent.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, list["EditContent"]]]:
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
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> Response[Union[HTTPValidationError, list["EditContent"]]]:
    """Get Edit Contents For Run

     Gets the data for all edits in a run.

    Equivalent logic to /edits/edit_id/content except for all edits in a run

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[None, Unset, str]):
        include_exported (Union[Unset, bool]):  Default: True.
        page_num (Union[Unset, int]):  Default: 0.
        meta_cols (Union[None, Unset, list[str]]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['EditContent']]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        split=split,
        inference_name=inference_name,
        include_exported=include_exported,
        page_num=page_num,
        meta_cols=meta_cols,
        text_pat=text_pat,
        regex=regex,
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[HTTPValidationError, list["EditContent"]]]:
    """Get Edit Contents For Run

     Gets the data for all edits in a run.

    Equivalent logic to /edits/edit_id/content except for all edits in a run

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[None, Unset, str]):
        include_exported (Union[Unset, bool]):  Default: True.
        page_num (Union[Unset, int]):  Default: 0.
        meta_cols (Union[None, Unset, list[str]]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['EditContent']]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        split=split,
        client=client,
        inference_name=inference_name,
        include_exported=include_exported,
        page_num=page_num,
        meta_cols=meta_cols,
        text_pat=text_pat,
        regex=regex,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> Response[Union[HTTPValidationError, list["EditContent"]]]:
    """Get Edit Contents For Run

     Gets the data for all edits in a run.

    Equivalent logic to /edits/edit_id/content except for all edits in a run

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[None, Unset, str]):
        include_exported (Union[Unset, bool]):  Default: True.
        page_num (Union[Unset, int]):  Default: 0.
        meta_cols (Union[None, Unset, list[str]]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['EditContent']]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        split=split,
        inference_name=inference_name,
        include_exported=include_exported,
        page_num=page_num,
        meta_cols=meta_cols,
        text_pat=text_pat,
        regex=regex,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    inference_name: Union[None, Unset, str] = UNSET,
    include_exported: Union[Unset, bool] = True,
    page_num: Union[Unset, int] = 0,
    meta_cols: Union[None, Unset, list[str]] = UNSET,
    text_pat: Union[None, Unset, str] = UNSET,
    regex: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[HTTPValidationError, list["EditContent"]]]:
    """Get Edit Contents For Run

     Gets the data for all edits in a run.

    Equivalent logic to /edits/edit_id/content except for all edits in a run

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[None, Unset, str]):
        include_exported (Union[Unset, bool]):  Default: True.
        page_num (Union[Unset, int]):  Default: 0.
        meta_cols (Union[None, Unset, list[str]]):
        text_pat (Union[None, Unset, str]):
        regex (Union[None, Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['EditContent']]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            split=split,
            client=client,
            inference_name=inference_name,
            include_exported=include_exported,
            page_num=page_num,
            meta_cols=meta_cols,
            text_pat=text_pat,
            regex=regex,
        )
    ).parsed
