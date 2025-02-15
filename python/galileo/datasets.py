from typing import Union, Dict, Any
import mimetypes

from galileo.models.dataset_db import DatasetDB
from galileo.models.list_dataset_params import ListDatasetParams
from galileo.models.list_dataset_response import ListDatasetResponse
from galileo.models.dataset_name_filter import DatasetNameFilter
from galileo.models.dataset_name_filter_operator import DatasetNameFilterOperator
from galileo.api.datasets import (
    list_datasets_datasets_get,
    query_datasets_datasets_query_post,
    get_dataset_content_datasets_dataset_id_content_get,
    update_dataset_content_datasets_dataset_id_content_patch,
    delete_dataset_datasets_dataset_id_delete,
    upload_dataset_datasets_post,
)
from galileo.models.dataset_updated_at_sort import DatasetUpdatedAtSort
from galileo.models.dataset_content import DatasetContent
from galileo.models.update_dataset_content_request import UpdateDatasetContentRequest

from galileo.models.dataset_update_row import DatasetUpdateRow
from galileo.models.dataset_update_row_values import DatasetUpdateRowValues
from galileo.models.http_validation_error import HTTPValidationError
from galileo.models.body_upload_dataset_datasets_post import (
    BodyUploadDatasetDatasetsPost,
)
from galileo.types import Unset, File

from galileo_core.utils.dataset import DatasetType, parse_dataset

from galileo.base import BaseClientModel


class Dataset(BaseClientModel):
    content: DatasetContent | None = None

    def __init__(self, dataset_db: DatasetDB) -> None:
        self._dataset = dataset_db

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
        if not self._dataset:
            return None

        content: DatasetContent = (
            get_dataset_content_datasets_dataset_id_content_get.sync(
                client=self._get_client(), dataset_id=self._dataset.id
            )
        )

        self.content = content

        return content

    def add_rows(self, row_data: list[Dict[str, Any]]) -> "Dataset":
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
                client=self._get_client(), dataset_id=self._dataset.id, body=request
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
        return getattr(self._dataset, attr)


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
        datasets: ListDatasetResponse = list_datasets_datasets_get.sync(
            client=self._get_client(), limit=limit
        )
        return [Dataset(dataset) for dataset in datasets.datasets] if datasets else []

    def get(self, name: str, with_content: bool = False) -> Dataset | None:
        """
        Gets a dataset by name.

        Parameters
        ----------
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
        filter = DatasetNameFilter(operator=DatasetNameFilterOperator.EQ, value=name)
        params = ListDatasetParams(
            filters=[filter], sort=DatasetUpdatedAtSort(ascending=False)
        )
        datasets: ListDatasetResponse = query_datasets_datasets_query_post.sync(
            client=self._get_client(), body=params, limit=1
        )

        if datasets and len(datasets.datasets) > 0:
            dataset = Dataset(datasets.datasets[0])

            if with_content:
                dataset.get_content()
            return dataset
        else:
            return None

    def delete(self, name: str) -> None:
        """
        Deletes a dataset by name.

        Parameters
        ----------
        name : str
            The name of the dataset.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        dataset = self.get(name=name)
        if not dataset:
            raise ValueError(f"Dataset {name} not found")
        return delete_dataset_datasets_dataset_id_delete.sync(
            client=self._get_client(), dataset_id=dataset.id
        )

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

        response = upload_dataset_datasets_post.sync(
            client=self._get_client(), body=body, format_=dataset_format
        )

        if isinstance(response, HTTPValidationError):
            raise response

        if not response:
            raise ValueError("Unable to create dataset")

        return Dataset(response)


#
# Convenience methods
#


def get_dataset(name: str) -> Dataset | None:
    """
    Gets a dataset by name.

    Parameters
    ----------
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
    return Datasets().get(name=name)


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


def delete_dataset(name: str) -> None:
    """
    Deletes a dataset by name.

    Parameters
    ----------
    name : str
        The name of the dataset.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Datasets().delete(name=name)


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
