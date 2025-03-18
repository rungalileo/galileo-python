import mimetypes
from typing import Any, Optional, Union, overload

from galileo.api_client import GalileoApiClient
from galileo.base import BaseClientModel
from galileo.resources.api.datasets import (
    delete_dataset_datasets_dataset_id_delete,
    get_dataset_content_datasets_dataset_id_content_get,
    get_dataset_datasets_dataset_id_get,
    list_datasets_datasets_get,
    query_datasets_datasets_query_post,
    update_dataset_content_datasets_dataset_id_content_patch,
    upload_dataset_datasets_post,
)
from galileo.resources.models.body_upload_dataset_datasets_post import BodyUploadDatasetDatasetsPost
from galileo.resources.models.dataset_content import DatasetContent
from galileo.resources.models.dataset_db import DatasetDB
from galileo.resources.models.dataset_name_filter import DatasetNameFilter
from galileo.resources.models.dataset_name_filter_operator import DatasetNameFilterOperator
from galileo.resources.models.dataset_update_row import DatasetUpdateRow
from galileo.resources.models.dataset_update_row_values import DatasetUpdateRowValues
from galileo.resources.models.dataset_updated_at_sort import DatasetUpdatedAtSort
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.list_dataset_params import ListDatasetParams
from galileo.resources.models.list_dataset_response import ListDatasetResponse
from galileo.resources.models.update_dataset_content_request import UpdateDatasetContentRequest
from galileo.resources.types import File, Unset
from galileo.utils.catch_log import DecorateAllMethods
from galileo_core.utils.dataset import DatasetType, parse_dataset


class Dataset(BaseClientModel, DecorateAllMethods):
    content: Optional[DatasetContent] = None

    def __init__(self, dataset_db: DatasetDB, client: Optional[GalileoApiClient] = None) -> None:
        self.dataset = dataset_db
        super().__init__(client=client)

    def get_content(self) -> Union[None, DatasetContent]:
        """
        Gets and returns the content of the dataset.
        Also refreshes the content of the local dataset instance.

        Returns
        -------
        Union[None, DatasetContent]
            The content of the dataset

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        if not self.dataset:
            return None

        content: DatasetContent = get_dataset_content_datasets_dataset_id_content_get.sync(
            client=self.client, dataset_id=self.dataset.id
        )

        self.content = content

        return content

    def add_rows(self, row_data: list[dict[str, Any]]) -> "Dataset":
        """
        Adds rows to the dataset.

        Parameters
        ----------
        row_data : list[Dict[str, Any]]
            The rows to add to the dataset.

        Returns
        -------
        Dataset
            The updated dataset with the new rows.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        for row in row_data:
            row_values = DatasetUpdateRow(values=DatasetUpdateRowValues.from_dict(row))
            request = UpdateDatasetContentRequest(edits=[row_values])
            response = update_dataset_content_datasets_dataset_id_content_patch.sync(
                client=self.client, dataset_id=self.dataset.id, body=request
            )
            if isinstance(response, HTTPValidationError):
                raise response

        # Refresh the content
        self.get_content()

        return self

    def __getattr__(self, attr):
        """
        Delegate attribute access to the underlying DatasetDB instance.
        """
        return getattr(self.dataset, attr)


class Datasets(BaseClientModel):
    def list(self, limit: Union[Unset, int] = 100) -> list[Dataset]:
        """
        Lists all datasets.

        Parameters
        ----------
        limit : Union[Unset, int]
            The maximum number of datasets to return. Default is 100.

        Returns
        -------
        list[Dataset]
            A list of datasets.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        datasets: ListDatasetResponse = list_datasets_datasets_get.sync(client=self.client, limit=limit)
        return [Dataset(dataset_db=dataset, client=self.client) for dataset in datasets.datasets] if datasets else []

    @overload
    def get(self, *, id: str, with_content: bool = False) -> Optional[Dataset]: ...
    @overload
    @overload
    def get(self, *, name: str, with_content: bool = False) -> Optional[Dataset]: ...
    def get(
        self, *, id: Optional[str] = None, name: Optional[str] = None, with_content: bool = False
    ) -> Optional[Dataset]:
        """
        Retrieves a dataset by id or name (exactly one of `id` or `name` must be provided).

        Parameters
        ----------
        id : str
            The id of the dataset.
        name : str
            The name of the dataset.
        with_content : bool
            Whether to return the content of the dataset. Default is False.

        Returns
        -------
        Dataset
            The dataset.

        Raises
        ------
        ValueError
            If neither or both `id` and `name` are provided.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        if (id is None) == (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        if id:
            dataset_response = get_dataset_datasets_dataset_id_get.sync(client=self.client, dataset_id=id)
            if not dataset_response:
                return None
            dataset = Dataset(dataset_db=dataset_response, client=self.client)

        elif name:
            filter = DatasetNameFilter(operator=DatasetNameFilterOperator.EQ, value=name)
            params = ListDatasetParams(filters=[filter], sort=DatasetUpdatedAtSort(ascending=False))
            datasets_response: ListDatasetResponse = query_datasets_datasets_query_post.sync(
                client=self.client, body=params, limit=1
            )

            if not datasets_response or len(datasets_response.datasets) == 0:
                return None

            dataset = Dataset(dataset_db=datasets_response.datasets[0], client=self.client)

        if with_content:
            dataset.get_content()
        return dataset

    @overload
    def delete(self, *, id: str) -> None: ...
    @overload
    def delete(self, *, name: str) -> None: ...
    def delete(self, *, id: Optional[str] = None, name: Optional[str] = None) -> None:
        """
        Deletes a dataset by id or name.

        Parameters
        ----------
        id : str
            The id of the dataset.
        name : str
            The name of the dataset.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        if (id is None) == (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        dataset = self.get(id=id, name=name)
        if not dataset:
            raise ValueError(f"Dataset {name} not found")
        return delete_dataset_datasets_dataset_id_delete.sync(client=self.client, dataset_id=dataset.id)

    def create(self, name: str, content: DatasetType) -> Dataset:
        """
        Creates a new dataset.

        Parameters
        ----------
        name : str
            The name of the dataset.
        content : DatasetType
            The content of the dataset.

        Returns
        -------
        Dataset
            The created dataset.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """

        file_path, dataset_format = parse_dataset(content)
        file = File(
            payload=file_path.open("rb"),
            file_name=name,
            mime_type=mimetypes.guess_type(file_path)[0] or "application/octet-stream",
        )

        body = BodyUploadDatasetDatasetsPost(file=file)

        response = upload_dataset_datasets_post.sync(client=self.client, body=body, format_=dataset_format)

        if isinstance(response, HTTPValidationError):
            raise response

        if not response:
            raise ValueError("Unable to create dataset")

        return Dataset(dataset_db=response, client=self.client)


#
# Convenience methods
#


def get_dataset(*, id: Optional[str] = None, name: Optional[str] = None) -> Optional[Dataset]:
    """
    Retrieves a dataset by id or name (exactly one of `id` or `name` must be provided).

    Parameters
    ----------
    id : str
        The id of the dataset.
    name : str
        The name of the dataset.
    with_content : bool
        Whether to return the content of the dataset. Default is False.

    Returns
    -------
    Dataset
        The dataset.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Datasets().get(id=id, name=name)


def list_datasets(limit: Union[Unset, int] = 100) -> list[Dataset]:
    """
    Lists all datasets.

    Parameters
    ----------
    limit : Union[Unset, int]
        The maximum number of datasets to return. Default is 100.

    Returns
    -------
    list[Dataset]
        A list of datasets.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Datasets().list(limit=limit)


def delete_dataset(*, id: Optional[str] = None, name: Optional[str] = None) -> None:
    """
    Deletes a dataset by id or name (exactly one of `id` or `name` must be provided).

    Parameters
    ----------
    id : str
        The id of the dataset.
    name : str
        The name of the dataset.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Datasets().delete(id=id, name=name)


def create_dataset(name: str, content: DatasetType) -> Dataset:
    """
    Creates a new dataset.

    Parameters
    ----------
    name : str
        The name of the dataset.
    content : DatasetType
        The content of the dataset.

    Returns
    -------
    Dataset
        The created dataset.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Datasets().create(name=name, content=content)


def convert_dataset_content_to_records(dataset_content: DatasetContent):
    rows = dataset_content.rows
    if not rows:
        return []
    return [row.additional_properties["values_dict"] for row in rows]
