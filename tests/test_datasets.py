import json
from http import HTTPStatus
from unittest.mock import ANY, Mock, patch
from uuid import uuid4

import pytest

from galileo.datasets import (
    Dataset,
    DatasetAPIException,
    DatasetAppendRow,
    DatasetAppendRowValues,
    Datasets,
    UpdateDatasetContentRequest,
    convert_dataset_row_to_record,
    create_dataset,
    get_dataset_version,
    get_dataset_version_history,
)
from galileo.resources.models import (
    DatasetContent,
    DatasetDB,
    DatasetNameFilter,
    DatasetNameFilterOperator,
    DatasetUpdatedAtSort,
    ListDatasetParams,
    ListDatasetResponse,
    ListDatasetVersionParams,
    ListDatasetVersionResponse,
)
from galileo.resources.models.dataset_row import DatasetRow
from galileo.resources.models.dataset_row_values_dict import DatasetRowValuesDict
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.types import Response
from galileo.schema.datasets import DatasetRecord


def dataset_content():
    row = DatasetRow(
        index=0,
        values=["Which continent is Spain in?", "Europe"],
        metadata=None,
        row_id="",
        values_dict={"input": "Which continent is Spain in?", "expected": "Europe"},
    )
    column_names = ["input", "expected"]
    return DatasetContent(column_names=column_names, rows=[row])


def dataset_db():
    return DatasetDB.from_dict(
        {
            "draft": False,
            "column_names": ["input", "output", "metadata"],
            "created_at": "2025-03-10T15:25:03.088471+00:00",
            "created_by_user": {
                # "email": "andriisoldatenko@galileo.ai",
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
                        # "email": "andriisoldatenko@galileo.ai",
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


def list_dataset_versions():
    return ListDatasetVersionResponse.from_dict(
        {
            "versions": [
                {
                    "column_names": ["input", "output", "metadata"],
                    "columns_added": 2,
                    "columns_removed": 1,
                    "columns_renamed": 0,
                    "created_at": "2025-03-26T12:00:44.553576+00:00",
                    "created_by_user": None,
                    "name": "JSON column migration",
                    "num_rows": 2,
                    "rows_added": 0,
                    "rows_edited": 2,
                    "rows_removed": 0,
                    "version_index": 2,
                },
                {
                    "column_names": ["input", "expected"],
                    "columns_added": 2,
                    "columns_removed": 0,
                    "columns_renamed": 0,
                    "created_at": "2025-03-10T15:25:03.582730+00:00",
                    "created_by_user": {
                        "email": "andriisoldatenko@galileo.ai",
                        "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                        "first_name": "",
                        "last_name": "",
                    },
                    "name": None,
                    "num_rows": 2,
                    "rows_added": 2,
                    "rows_edited": 0,
                    "rows_removed": 0,
                    "version_index": 1,
                },
            ],
            "limit": 100,
            "next_starting_token": None,
            "paginated": False,
            "starting_token": 0,
        }
    )


@patch("galileo.datasets.create_dataset_datasets_post")
def test_create_dataset_validation_error(create_dataset_datasets_post_mock: Mock):
    create_dataset_datasets_post_mock.sync_detailed.return_value = Response(
        content=b'{"detail":"Invalid CSV data: CSV parse error: Empty CSV file or block: cannot infer number of columns"}',
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        headers={},
        parsed=None,
    )

    with pytest.raises(DatasetAPIException):
        create_dataset(name="my_dataset_name", content=[{}])

    create_dataset_datasets_post_mock.sync_detailed.assert_called_once()


@patch("galileo.datasets.get_dataset_version_content_datasets_dataset_id_versions_version_index_content_get")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
def test_get_dataset_version_using_dataset_id(
    get_dataset_datasets_dataset_id_get: Mock, get_dataset_version_mock: Mock
):
    get_dataset_datasets_dataset_id_get.sync.return_value = dataset_db()
    get_dataset_version_mock.sync.return_value = dataset_content()

    result = get_dataset_version(version_index=1, dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9")
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

    result = get_dataset_version(version_index=1, dataset_name="test")
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


@patch("galileo.datasets.query_dataset_versions_datasets_dataset_id_versions_query_post")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
def test_get_dataset_version_history_using_dataset_id(
    get_dataset_datasets_dataset_id_get: Mock, get_dataset_versions_mock: Mock
):
    get_dataset_datasets_dataset_id_get.sync.return_value = dataset_db()
    get_dataset_versions_mock.sync.return_value = list_dataset_versions()

    ds_history = get_dataset_version_history(dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9")

    assert ds_history == list_dataset_versions()
    get_dataset_datasets_dataset_id_get.sync.assert_called_once_with(
        client=ANY, dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9"
    )

    get_dataset_versions_mock.sync.assert_called_once_with(
        client=ANY, dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9", body=ListDatasetVersionParams()
    )


@patch("galileo.datasets.query_dataset_versions_datasets_dataset_id_versions_query_post")
@patch("galileo.datasets.query_datasets_datasets_query_post")
def test_get_dataset_version_history_using_dataset_name(
    query_datasets_datasets_query_post: Mock, get_dataset_version_mock: Mock
):
    query_datasets_datasets_query_post.sync.return_value = dataset_response()
    get_dataset_version_mock.sync.return_value = list_dataset_versions()

    ds_history = get_dataset_version_history(dataset_name="test")

    assert ds_history == list_dataset_versions()
    ds_name_filter = DatasetNameFilter(operator=DatasetNameFilterOperator.EQ, value="test")
    body = ListDatasetParams(filters=[ds_name_filter], sort=DatasetUpdatedAtSort(ascending=False))
    query_datasets_datasets_query_post.sync.assert_called_once_with(client=ANY, body=body, limit=1)

    # load dataset always by dataset_id
    get_dataset_version_mock.sync.assert_called_once_with(
        client=ANY, dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9", body=ListDatasetVersionParams()
    )


def test_get_dataset_version_history_wo_dataset_name_or_dataset_id():
    with pytest.raises(ValueError) as exc_info:
        get_dataset_version_history()
    assert "Either dataset_name or dataset_id must be provided." in str(exc_info.value), str(exc_info)


def test_convert_dataset_row_to_record():
    """Test the convert_dataset_row_to_record function with various inputs."""

    # Case 1: Normal case with input, output, and metadata
    values_dict = DatasetRowValuesDict()
    values_dict["input"] = "Which continent is Spain in?"
    values_dict["output"] = "Europe"
    values_dict["metadata"] = json.dumps({"confidence": "high"})
    row = DatasetRow(
        index=0,
        values=["Which continent is Spain in?", "Europe", json.dumps({"confidence": "high"})],
        metadata=None,
        row_id="row1",
        values_dict=values_dict,
    )
    record = convert_dataset_row_to_record(row)
    assert isinstance(record, DatasetRecord)
    assert record.id == "row1"
    assert record.input == "Which continent is Spain in?"
    assert record.output == "Europe"
    assert record.metadata == {"confidence": "high"}

    # Case 2: With input but no output
    values_dict = DatasetRowValuesDict()
    values_dict["input"] = "Which continent is Spain in?"
    row = DatasetRow(
        index=0, values=["Which continent is Spain in?"], metadata=None, row_id="row2", values_dict=values_dict
    )
    record = convert_dataset_row_to_record(row)
    assert record.id == "row2"
    assert record.input == "Which continent is Spain in?"
    assert record.output is None
    assert record.metadata is None

    # Case 3: With input and metadata but no output
    values_dict = DatasetRowValuesDict()
    values_dict["input"] = "Which continent is Spain in?"
    values_dict["metadata"] = json.dumps({"source": "geography"})
    row = DatasetRow(
        index=0,
        values=["Which continent is Spain in?", None, json.dumps({"source": "geography"})],
        metadata=None,
        row_id="row3",
        values_dict=values_dict,
    )
    record = convert_dataset_row_to_record(row)
    assert record.id == "row3"
    assert record.input == "Which continent is Spain in?"
    assert record.output is None
    assert record.metadata == {"source": "geography"}

    # Case 4: With input that is not a string (should be converted to string)
    values_dict = DatasetRowValuesDict()
    values_dict["input"] = {"question": "Which continent is Spain in?"}
    row = DatasetRow(
        index=0,
        values=[{"question": "Which continent is Spain in?"}],
        metadata=None,
        row_id="row4",
        values_dict=values_dict,
    )
    record = convert_dataset_row_to_record(row)
    assert record.id == "row4"
    assert record.input == json.dumps({"question": "Which continent is Spain in?"})
    assert record.output is None
    assert record.metadata is None

    # Case 5: Missing input (should raise ValueError)
    values_dict = DatasetRowValuesDict()
    row = DatasetRow(index=0, values=[], metadata=None, row_id="row5", values_dict=values_dict)
    with pytest.raises(ValueError, match="Dataset row must have input field"):
        convert_dataset_row_to_record(row)

    # Case 6: Empty input (should raise ValueError)
    values_dict = DatasetRowValuesDict()
    values_dict["input"] = ""
    row = DatasetRow(index=0, values=[""], metadata=None, row_id="row6", values_dict=values_dict)
    with pytest.raises(ValueError, match="Dataset row must have input field"):
        convert_dataset_row_to_record(row)


@patch("galileo.datasets.get_dataset_content_datasets_dataset_id_content_get")
def test__get_etag(get_dataset_content_by_id_patch: Mock) -> None:
    mock_client = Mock()
    dataset = Dataset(dataset_db=dataset_db(), client=mock_client)

    expected_etag: str = str(uuid4())
    mock_response = Mock()
    mock_response.headers = {"ETag": expected_etag}
    get_dataset_content_by_id_patch.sync_detailed.return_value = mock_response

    assert expected_etag == dataset._get_etag()
    get_dataset_content_by_id_patch.sync_detailed.assert_called_once_with(
        client=mock_client, dataset_id=dataset.dataset.id
    )


@patch("galileo.datasets.Dataset._get_etag", return_value="test_etag")
@patch("galileo.datasets.get_dataset_content_datasets_dataset_id_content_get")
@patch("galileo.datasets.update_dataset_content_datasets_dataset_id_content_patch")
def test_dataset_add_rows_success(update_dataset_patch: Mock, get_dataset_content_patch: Mock, etag_patch: Mock):
    mock_client = Mock()
    dataset = Dataset(dataset_db=dataset_db(), client=mock_client)

    dataset.add_rows([{"input": "b"}, {"input": "c"}])

    expected_append_row_b = DatasetAppendRowValues()
    expected_append_row_b.additional_properties = {"input": "b"}
    expected_append_row_c = DatasetAppendRowValues()
    expected_append_row_c.additional_properties = {"input": "c"}
    update_dataset_patch.sync.assert_called_once_with(
        client=mock_client,
        dataset_id="78e8035d-c429-47f2-8971-68f10e7e91c9",
        body=UpdateDatasetContentRequest(
            edits=[
                DatasetAppendRow(values=expected_append_row_b, edit_type="append_row"),
                DatasetAppendRow(values=expected_append_row_c, edit_type="append_row"),
            ]
        ),
        if_match="test_etag",
    )
    etag_patch.assert_called_once()
    get_dataset_content_patch.sync.assert_called_once()


@patch("galileo.datasets.Dataset._get_etag", return_value="test_etag")
@patch("galileo.datasets.get_dataset_content_datasets_dataset_id_content_get")
@patch("galileo.datasets.update_dataset_content_datasets_dataset_id_content_patch")
def test_dataset_add_rows_failure(update_dataset_patch: Mock, get_dataset_content_patch: Mock, etag_patch: Mock):
    update_dataset_patch.sync.return_value = HTTPValidationError()

    mock_client = Mock()
    dataset = Dataset(dataset_db=dataset_db(), client=mock_client)

    # NOTE: This method raises an exception. The reason we don't see one here is we catch all
    # exceptions and log them as errors in error log.
    dataset.add_rows([{"input": "b"}, {"input": "c"}])

    update_dataset_patch.sync.assert_called_once()
    etag_patch.assert_called_once()
    get_dataset_content_patch.sync.assert_not_called()


def test_delete_dataset_validation_errors():
    with pytest.raises(ValueError) as exc_info:
        Datasets().delete()
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        Datasets().delete(id=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        Datasets().delete(name=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"


def test_get_dataset_validation_errors():
    with pytest.raises(ValueError) as exc_info:
        Datasets().get()
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        Datasets().get(id=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        Datasets().get(name=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"
