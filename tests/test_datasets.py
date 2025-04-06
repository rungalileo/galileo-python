from unittest.mock import ANY, Mock, patch

import pytest

from galileo.datasets import get_dataset_version
from galileo.resources.models import (
    DatasetContent,
    DatasetDB,
    DatasetNameFilter,
    DatasetNameFilterOperator,
    DatasetRow,
    DatasetUpdatedAtSort,
    ListDatasetParams,
    ListDatasetResponse,
)


def dataset_content():
    row = DatasetRow(index=0, values=["Which continent is Spain in?", "Europe"])
    row.additional_properties = {"values_dict": {"input": "Which continent is Spain in?", "expected": "Europe"}}

    column_names = ["input", "expected"]
    return DatasetContent(column_names=column_names, rows=[row])


def dataset_db():
    return DatasetDB.from_dict(
        {
            "draft": False,
            "column_names": ["input", "output", "metadata"],
            "created_at": "2025-03-10T15:25:03.088471+00:00",
            "created_by_user": {
                "email": "andriisoldatenko@galileo.ai",
                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                "first_name": "",
                "last_name": "",
            },
            "current_version_index": 2,
            "id": "78e8035d-c429-47f2-8971-68f10e7e91c9",
            "name": "storyteller-dataset",
            "num_rows": 2,
            "project_count": 2,
            "updated_at": "2025-03-26T12:00:44.558105+00:00",
            "permissions": [],
        }
    )


def dataset_response():
    return ListDatasetResponse.from_dict(
        {
            "datasets": [
                {
                    "draft": False,
                    "column_names": ["input", "output", "metadata"],
                    "created_at": "2025-03-10T15:25:03.088471+00:00",
                    "created_by_user": {
                        "email": "andriisoldatenko@galileo.ai",
                        "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                        "first_name": "",
                        "last_name": "",
                    },
                    "current_version_index": 2,
                    "id": "78e8035d-c429-47f2-8971-68f10e7e91c9",
                    "name": "storyteller-dataset",
                    "num_rows": 2,
                    "project_count": 2,
                    "updated_at": "2025-03-26T12:00:44.558105+00:00",
                    "permissions": [],
                }
            ],
            "limit": 1,
            "next_starting_token": 1,
            "paginated": True,
            "starting_token": 0,
        }
    )


@patch("galileo.datasets.get_dataset_version_content_datasets_dataset_id_versions_version_index_content_get")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
def test_get_dataset_version_using_dataset_id(
    get_dataset_datasets_dataset_id_get: Mock, get_dataset_version_mock: Mock
):
    get_dataset_datasets_dataset_id_get.sync.return_value = dataset_db()
    get_dataset_version_mock.sync.return_value = dataset_content()

    result = get_dataset_version(1, dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9")
    assert result == dataset_content()

    get_dataset_datasets_dataset_id_get.sync.assert_called_once_with(
        client=ANY, dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9"
    )
    get_dataset_version_mock.sync.assert_called_once_with(
        client=ANY, version_index=1, dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9"
    )


@patch("galileo.datasets.get_dataset_version_content_datasets_dataset_id_versions_version_index_content_get")
@patch("galileo.datasets.query_datasets_datasets_query_post")
def test_get_dataset_version_using_dataset_name(
    query_datasets_datasets_query_post: Mock, get_dataset_version_mock: Mock
):
    query_datasets_datasets_query_post.sync.return_value = dataset_response()
    get_dataset_version_mock.sync.return_value = dataset_content()

    result = get_dataset_version(1, dataset_name="test")
    assert result == dataset_content()

    ds_name_filter = DatasetNameFilter(operator=DatasetNameFilterOperator.EQ, value="test")
    body = ListDatasetParams(filters=[ds_name_filter], sort=DatasetUpdatedAtSort(ascending=False))
    query_datasets_datasets_query_post.sync.assert_called_once_with(client=ANY, body=body, limit=1)
    # load dataset always by dataset_id
    get_dataset_version_mock.sync.assert_called_once_with(
        client=ANY, version_index=1, dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9"
    )


def test_get_dataset_version_wo_dataset_name_or_dataset_id():
    with pytest.raises(ValueError) as exc_info:
        get_dataset_version(version_index=1)
    assert "Either dataset_name or dataset_id must be provided." in str(exc_info.value), str(exc_info)
