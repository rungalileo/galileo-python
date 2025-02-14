from typing import Union

from galileo.models.dataset_db import DatasetDB
from galileo.models.list_dataset_params import ListDatasetParams
from galileo.models.list_dataset_response import ListDatasetResponse
from galileo.models.dataset_name_filter import DatasetNameFilter
from galileo.models.dataset_name_filter_operator import DatasetNameFilterOperator
from galileo.api.datasets import (
    list_datasets_datasets_get,
    query_datasets_datasets_query_post,
)
from galileo.models.dataset_updated_at_sort import DatasetUpdatedAtSort
from galileo.types import Unset

from galileo.base import BaseClientModel


class Dataset:
    def __init__(self, dataset_db: DatasetDB) -> None:
        self._dataset = dataset_db

    def add_row(self, row_data: dict) -> "Dataset":
        # TODO: implement
        return Dataset()

    def __getattr__(self, attr):
        """
        Delegate attribute access to the underlying DatasetDB instance.
        """
        return getattr(self._dataset, attr)


class Datasets(BaseClientModel):
    def list(self, limit: Union[Unset, int] = 100) -> list[Dataset]:
        datasets: ListDatasetResponse = list_datasets_datasets_get.sync(
            client=self._get_client(), limit=limit
        )
        return [Dataset(dataset) for dataset in datasets.datasets] if datasets else []

    def get(self, name: str) -> Dataset | None:
        filter = DatasetNameFilter(operator=DatasetNameFilterOperator.EQ, value=name)
        params = ListDatasetParams(
            filters=[filter], sort=DatasetUpdatedAtSort(ascending=False)
        )
        datasets: ListDatasetResponse = query_datasets_datasets_query_post.sync(
            client=self._get_client(), body=params, limit=1
        )

        if datasets and len(datasets.datasets) > 0:
            return Dataset(datasets.datasets[0])
        else:
            return None


#
# Convenience methods
#


def get_dataset(name: str) -> Dataset | None:
    return Datasets().get(name=name)


def list_datasets(limit: Union[Unset, int] = 100) -> list[Dataset]:
    return Datasets().list(limit=limit)
