from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.embedding_request import EmbeddingRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    body: EmbeddingRequest,
    inference_name: Union[Unset, str] = "",
    data_view: Union[Unset, bool] = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["inference_name"] = inference_name

    params["data_view"] = data_view

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/embeddings",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    split: Split,
    *,
    client: AuthenticatedClient,
    body: EmbeddingRequest,
    inference_name: Union[Unset, str] = "",
    data_view: Union[Unset, bool] = False,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Embeddings

     Get all embedding data for 500k (or otherwise requested) data points.

    This will take a random sample of the dataset. It exports the result as a csv
    in order to reduce request size and response latency (as results can be large)
    This will return:
    * id
    * gold (index)
    * prediction (index)
    * data quality
    * text_sample
    * x coordinate
    * y coordinate
    ** any metadata columns explicitly requested

    Set data_view=true to return data embeddings instead of model embeddings. If
    data embeddings are not available, an exception will be thrown

    Set use_seed=false for random batches of embeddings on every response. This is
    useful for batching, but should remain true if you are requesting a single set
    of embeddings. If you are returning all embeddings, this parameter is useless

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        data_view (Union[Unset, bool]):  Default: False.
        body (EmbeddingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id, run_id=run_id, split=split, body=body, inference_name=inference_name, data_view=data_view
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: EmbeddingRequest,
    inference_name: Union[Unset, str] = "",
    data_view: Union[Unset, bool] = False,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Embeddings

     Get all embedding data for 500k (or otherwise requested) data points.

    This will take a random sample of the dataset. It exports the result as a csv
    in order to reduce request size and response latency (as results can be large)
    This will return:
    * id
    * gold (index)
    * prediction (index)
    * data quality
    * text_sample
    * x coordinate
    * y coordinate
    ** any metadata columns explicitly requested

    Set data_view=true to return data embeddings instead of model embeddings. If
    data embeddings are not available, an exception will be thrown

    Set use_seed=false for random batches of embeddings on every response. This is
    useful for batching, but should remain true if you are requesting a single set
    of embeddings. If you are returning all embeddings, this parameter is useless

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        data_view (Union[Unset, bool]):  Default: False.
        body (EmbeddingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        split=split,
        client=client,
        body=body,
        inference_name=inference_name,
        data_view=data_view,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: EmbeddingRequest,
    inference_name: Union[Unset, str] = "",
    data_view: Union[Unset, bool] = False,
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Embeddings

     Get all embedding data for 500k (or otherwise requested) data points.

    This will take a random sample of the dataset. It exports the result as a csv
    in order to reduce request size and response latency (as results can be large)
    This will return:
    * id
    * gold (index)
    * prediction (index)
    * data quality
    * text_sample
    * x coordinate
    * y coordinate
    ** any metadata columns explicitly requested

    Set data_view=true to return data embeddings instead of model embeddings. If
    data embeddings are not available, an exception will be thrown

    Set use_seed=false for random batches of embeddings on every response. This is
    useful for batching, but should remain true if you are requesting a single set
    of embeddings. If you are returning all embeddings, this parameter is useless

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        data_view (Union[Unset, bool]):  Default: False.
        body (EmbeddingRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id, run_id=run_id, split=split, body=body, inference_name=inference_name, data_view=data_view
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    split: Split,
    *,
    client: AuthenticatedClient,
    body: EmbeddingRequest,
    inference_name: Union[Unset, str] = "",
    data_view: Union[Unset, bool] = False,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Embeddings

     Get all embedding data for 500k (or otherwise requested) data points.

    This will take a random sample of the dataset. It exports the result as a csv
    in order to reduce request size and response latency (as results can be large)
    This will return:
    * id
    * gold (index)
    * prediction (index)
    * data quality
    * text_sample
    * x coordinate
    * y coordinate
    ** any metadata columns explicitly requested

    Set data_view=true to return data embeddings instead of model embeddings. If
    data embeddings are not available, an exception will be thrown

    Set use_seed=false for random batches of embeddings on every response. This is
    useful for batching, but should remain true if you are requesting a single set
    of embeddings. If you are returning all embeddings, this parameter is useless

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        inference_name (Union[Unset, str]):  Default: ''.
        data_view (Union[Unset, bool]):  Default: False.
        body (EmbeddingRequest):

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
            split=split,
            client=client,
            body=body,
            inference_name=inference_name,
            data_view=data_view,
        )
    ).parsed
