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
    extend_dataset,
    get_dataset_version,
    get_dataset_version_history,
)
from galileo.resources.models import (
    BodyCreateDatasetDatasetsPost,
    DatasetContent,
    DatasetDB,
    DatasetFormat,
    DatasetNameFilter,
    DatasetNameFilterOperator,
    DatasetUpdatedAtSort,
    JobProgress,
    ListDatasetParams,
    ListDatasetResponse,
    ListDatasetVersionParams,
    ListDatasetVersionResponse,
    SyntheticDatasetExtensionResponse,
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
def test_create_dataset_validation_error(create_dataset_datasets_post_mock: Mock) -> None:
    with pytest.raises(ValueError) as exc_info:
        create_dataset(name="my_dataset_name", content=None)
    assert "Invalid dataset type: '<class 'NoneType'>'." in str(exc_info.value), str(exc_info)


@patch("galileo.datasets.create_dataset_datasets_post")
def test_create_dataset_with_empty_list(create_dataset_datasets_post_mock: Mock) -> None:
    create_dataset_datasets_post_mock.sync_detailed.return_value = Response(
        content=b'{"id":"bb830fae-99d3-4ce7-bef9-300d528e0060","permissions":[],"name":"my_dataset_name","created_at":"2025-05-16T16:26:41.76451","email":"user.test@galileo.ai","first_name":"","last_name":""},"current_version_index":1,"draft":false}',
        status_code=HTTPStatus.OK,
        headers={},
        parsed=DatasetDB.from_dict(
            {
                "draft": False,
                "column_names": ["input", "output", "metadata"],
                "created_at": "2025-03-10T15:25:03.088471+00:00",
                "created_by_user": {"id": "01ce18ac-3960-46e1-bb79-0e4965069add"},
                "current_version_index": 1,
                "id": "bb830fae-99d3-4ce7-bef9-300d528e0060",
                "name": "my_dataset_name",
                "updated_at": "2025-03-26T12:00:44.558105+00:00",
                "num_rows": 1,
                "project_count": 0,
                "permissions": [],
            }
        ),
    )

    create_dataset(name="my_dataset_name", content=[])
    create_dataset_datasets_post_mock.sync_detailed.assert_called_once_with(
        client=ANY,
        body=BodyCreateDatasetDatasetsPost(draft=False, file=ANY, name="my_dataset_name"),
        format_=DatasetFormat.JSONL,
    )


@patch("galileo.datasets.create_dataset_datasets_post")
def test_create_dataset_with_empty_dict(create_dataset_datasets_post_mock: Mock) -> None:
    create_dataset_datasets_post_mock.sync_detailed.return_value = Response(
        content=b'{"id":"bb830fae-99d3-4ce7-bef9-300d528e0060","permissions":[],"name":"my_dataset_name","created_at":"2025-05-16T16:26:41.76451","email":"user.test@galileo.ai","first_name":"","last_name":""},"current_version_index":1,"draft":false}',
        status_code=HTTPStatus.OK,
        headers={},
        parsed=DatasetDB.from_dict(
            {
                "draft": False,
                "column_names": ["input", "output", "metadata"],
                "created_at": "2025-03-10T15:25:03.088471+00:00",
                "created_by_user": {"id": "01ce18ac-3960-46e1-bb79-0e4965069add"},
                "current_version_index": 1,
                "id": "bb830fae-99d3-4ce7-bef9-300d528e0060",
                "name": "my_dataset_name",
                "updated_at": "2025-03-26T12:00:44.558105+00:00",
                "num_rows": 1,
                "project_count": 0,
                "permissions": [],
            }
        ),
    )

    create_dataset(name="my_dataset_name", content={})
    create_dataset_datasets_post_mock.sync_detailed.assert_called_once_with(
        client=ANY,
        body=BodyCreateDatasetDatasetsPost(draft=False, file=ANY, name="my_dataset_name"),
        format_=DatasetFormat.JSONL,
    )


@patch("galileo.datasets.get_dataset_version_content_datasets_dataset_id_versions_version_index_content_get")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
def test_get_dataset_version_using_dataset_id(
    get_dataset_datasets_dataset_id_get: Mock, get_dataset_version_mock: Mock
) -> None:
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
) -> None:
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


def test_get_dataset_version_wo_dataset_name_or_dataset_id() -> None:
    with pytest.raises(ValueError) as exc_info:
        get_dataset_version(version_index=1)
    assert "Either dataset_name or dataset_id must be provided." in str(exc_info.value), str(exc_info)


@patch("galileo.datasets.query_dataset_versions_datasets_dataset_id_versions_query_post")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
def test_get_dataset_version_history_using_dataset_id(
    get_dataset_datasets_dataset_id_get: Mock, get_dataset_versions_mock: Mock
) -> None:
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
) -> None:
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


def test_get_dataset_version_history_wo_dataset_name_or_dataset_id() -> None:
    with pytest.raises(ValueError) as exc_info:
        get_dataset_version_history()
    assert "Either dataset_name or dataset_id must be provided." in str(exc_info.value), str(exc_info)


def test_convert_dataset_row_to_record() -> None:
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
    dataset = Dataset(dataset_db=dataset_db())

    expected_etag: str = str(uuid4())
    mock_response = Mock()
    mock_response.headers = {"ETag": expected_etag}
    get_dataset_content_by_id_patch.sync_detailed.return_value = mock_response

    assert expected_etag == dataset._get_etag()
    get_dataset_content_by_id_patch.sync_detailed.assert_called_once_with(
        client=dataset.config.api_client, dataset_id=dataset.dataset.id
    )


@patch("galileo.datasets.Dataset._get_etag", return_value="test_etag")
@patch("galileo.datasets.get_dataset_content_datasets_dataset_id_content_get")
@patch("galileo.datasets.update_dataset_content_datasets_dataset_id_content_patch")
def test_dataset_add_rows_success(
    update_dataset_patch: Mock, get_dataset_content_patch: Mock, etag_patch: Mock
) -> None:
    dataset = Dataset(dataset_db=dataset_db())

    dataset.add_rows([{"input": "b"}, {"input": "c"}])

    expected_append_row_b = DatasetAppendRowValues()
    expected_append_row_b.additional_properties = {"input": "b"}
    expected_append_row_c = DatasetAppendRowValues()
    expected_append_row_c.additional_properties = {"input": "c"}
    update_dataset_patch.sync.assert_called_once_with(
        client=dataset.config.api_client,
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
def test_dataset_add_rows_failure(
    update_dataset_patch: Mock, get_dataset_content_patch: Mock, etag_patch: Mock
) -> None:
    update_dataset_patch.sync.return_value = HTTPValidationError()

    dataset = Dataset(dataset_db=dataset_db())

    # NOTE: This method raises an exception. The reason we don't see one here is we catch all
    # exceptions and log them as errors in error log.
    dataset.add_rows([{"input": "b"}, {"input": "c"}])

    update_dataset_patch.sync.assert_called_once()
    etag_patch.assert_called_once()
    get_dataset_content_patch.sync.assert_not_called()


def test_delete_dataset_validation_errors() -> None:
    with pytest.raises(ValueError) as exc_info:
        Datasets().delete()
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        Datasets().delete(id=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        Datasets().delete(name=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"


def test_get_dataset_validation_errors() -> None:
    with pytest.raises(ValueError) as exc_info:
        Datasets().get()
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        Datasets().get(id=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        Datasets().get(name=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"


@patch("galileo.datasets.get_dataset_content_datasets_dataset_id_content_get")
@patch("galileo.datasets.get_dataset_synthetic_extend_status_datasets_extend_dataset_id_get")
@patch("galileo.datasets.extend_dataset_content_datasets_extend_post")
@patch("galileo.datasets.time.sleep")  # Mock sleep to avoid actual delays
def test_extend_dataset_success(
    sleep_mock: Mock, extend_dataset_mock: Mock, get_extend_status_mock: Mock, get_dataset_content_mock: Mock
) -> None:
    """Test the extend_dataset function with successful completion."""

    # Setup test data
    extended_dataset_id = "a8b3d8e0-5e0b-4b0f-8b3a-3b9f4b3d3b3a"

    # Mock the initial extend request response
    extend_response = SyntheticDatasetExtensionResponse(dataset_id=extended_dataset_id)
    extend_dataset_mock.sync.return_value = extend_response

    # Mock job progress responses - first incomplete, then complete
    progress_responses = [
        JobProgress(steps_completed=1, steps_total=3, progress_message="Processing"),
        JobProgress(steps_completed=2, steps_total=3, progress_message="Still processing"),
        JobProgress(steps_completed=3, steps_total=3, progress_message="Done"),
    ]
    get_extend_status_mock.sync.side_effect = progress_responses

    # Mock the final dataset content
    extended_row = DatasetRow(
        index=0,
        row_id="be4dcadf-a0a2-475e-91e4-7bd03fdf5de8",
        values=["Extended", "Row"],
        values_dict={"col1": "Extended", "col2": "Row"},
        metadata=None,
    )
    dataset_content = DatasetContent(column_names=["col1", "col2"], rows=[extended_row])
    get_dataset_content_mock.sync.return_value = dataset_content

    # Call the function
    result = extend_dataset(
        prompt_settings={"model_alias": "GPT-4o mini"},
        prompt="Financial planning assistant that helps clients design an investment strategy.",
        instructions="You are a financial planning assistant that helps clients design an investment strategy.",
        examples=["I want to invest $1000 per month."],
        data_types=["Prompt Injection"],
        count=3,
    )

    # Verify the result
    assert result == [extended_row]

    # Verify the API calls
    extend_dataset_mock.sync.assert_called_once()
    assert get_extend_status_mock.sync.call_count == 3  # Called 3 times before completion
    get_dataset_content_mock.sync.assert_called_once_with(client=ANY, dataset_id=extended_dataset_id)

    # Verify sleep was called between status checks
    assert sleep_mock.call_count == 2  # Called 2 times (between the 3 status checks)


@patch("galileo.datasets.extend_dataset_content_datasets_extend_post")
def test_extend_dataset_api_failure(extend_dataset_mock: Mock) -> None:
    """Test extend_dataset when the initial API call fails."""

    # Mock API failure
    extend_dataset_mock.sync.return_value = HTTPValidationError()

    # Call should raise DatasetAPIException
    with pytest.raises(DatasetAPIException, match="Request to extend dataset failed."):
        extend_dataset(prompt_settings={"model_alias": "GPT-4o mini"}, prompt="Test prompt", count=1)


# ===================================================================
# Project Association Tests for Dataset CRUD Operations
# ===================================================================


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.query_datasets_datasets_query_post")
def test_list_datasets_with_project_id(query_datasets_mock: Mock, get_project_mock: Mock) -> None:
    """Test listing datasets filtered by project_id."""
    from galileo.datasets import list_datasets
    from galileo.projects import Project
    from galileo.resources.models import ProjectDB

    project_id = "test-project-id"
    dataset_db = DatasetDB(
        id="dataset-1",
        name="Test Dataset",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )

    # Mock project retrieval
    project_db = ProjectDB(id=project_id, name="Test Project")
    get_project_mock.return_value = Project(project=project_db)

    # Mock dataset query response
    query_datasets_mock.sync.return_value = ListDatasetResponse(datasets=[dataset_db])

    # Call the function
    result = list_datasets(project_id=project_id, limit=100)

    # Verify results
    assert len(result) == 1
    assert result[0].id == "dataset-1"
    assert result[0].name == "Test Dataset"

    # Verify the API was called with project filter
    query_datasets_mock.sync.assert_called_once()
    call_args = query_datasets_mock.sync.call_args
    assert call_args.kwargs["body"].filters[0].value == project_id


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.query_datasets_datasets_query_post")
def test_list_datasets_with_project_name(query_datasets_mock: Mock, get_project_mock: Mock) -> None:
    """Test listing datasets filtered by project_name."""
    from galileo.datasets import list_datasets
    from galileo.projects import Project
    from galileo.resources.models import ProjectDB

    project_name = "Test Project"
    project_id = "test-project-id"
    dataset_db = DatasetDB(
        id="dataset-1",
        name="Test Dataset",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )

    # Mock project retrieval by name
    project_db = ProjectDB(id=project_id, name=project_name)
    get_project_mock.return_value = Project(project=project_db)

    # Mock dataset query response
    query_datasets_mock.sync.return_value = ListDatasetResponse(datasets=[dataset_db])

    # Call the function
    result = list_datasets(project_name=project_name, limit=100)

    # Verify results
    assert len(result) == 1
    assert result[0].id == "dataset-1"

    # Verify the API was called with resolved project_id
    query_datasets_mock.sync.assert_called_once()
    call_args = query_datasets_mock.sync.call_args
    assert call_args.kwargs["body"].filters[0].value == project_id


def test_list_datasets_with_both_project_params() -> None:
    """Test that providing both project_id and project_name raises an error."""
    from galileo.datasets import list_datasets

    with pytest.raises(ValueError, match="Only one of 'project_id' or 'project_name' can be provided, not both"):
        list_datasets(project_id="id-123", project_name="My Project")


@patch("galileo.projects.Projects.get")
def test_list_datasets_with_nonexistent_project_name(get_project_mock: Mock) -> None:
    """Test listing datasets with a project name that doesn't exist."""
    from galileo.datasets import list_datasets

    # Mock project not found
    get_project_mock.return_value = None

    with pytest.raises(ValueError, match="Project 'Nonexistent Project' does not exist"):
        list_datasets(project_name="Nonexistent Project")


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
@patch("galileo.resources.api.datasets.list_dataset_projects_datasets_dataset_id_projects_get.sync")
def test_get_dataset_with_project_id(list_projects_mock: Mock, get_dataset_mock: Mock, get_project_mock: Mock) -> None:
    """Test getting a dataset with project_id validation."""
    from galileo.datasets import get_dataset
    from galileo.projects import Project
    from galileo.resources.models import ListDatasetProjectsResponse, ProjectDB

    dataset_id = "dataset-1"
    project_id = "test-project-id"

    # Mock dataset retrieval
    dataset_db = DatasetDB(
        id=dataset_id,
        name="Test Dataset",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )
    get_dataset_mock.sync.return_value = dataset_db

    # Mock project retrieval
    project_db = ProjectDB(id=project_id, name="Test Project")
    get_project_mock.return_value = Project(project=project_db)

    # Mock dataset projects list
    list_projects_mock.return_value = ListDatasetProjectsResponse(
        projects=[ProjectDB(id=project_id, name="Test Project")]
    )

    # Call the function
    result = get_dataset(id=dataset_id, project_id=project_id)

    # Verify results
    assert result is not None
    assert result.id == dataset_id

    # Verify the project validation was called
    list_projects_mock.assert_called_once()


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.query_datasets_datasets_query_post")
@patch("galileo.resources.api.datasets.list_dataset_projects_datasets_dataset_id_projects_get.sync")
def test_get_dataset_with_project_name(
    list_projects_mock: Mock, query_datasets_mock: Mock, get_project_mock: Mock
) -> None:
    """Test getting a dataset with project_name validation."""
    from galileo.datasets import get_dataset
    from galileo.projects import Project
    from galileo.resources.models import ListDatasetProjectsResponse, ProjectDB

    dataset_name = "Test Dataset"
    dataset_id = "dataset-1"
    project_name = "Test Project"
    project_id = "test-project-id"

    # Mock dataset retrieval by name
    dataset_db = DatasetDB(
        id=dataset_id,
        name=dataset_name,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )
    query_datasets_mock.sync.return_value = ListDatasetResponse(datasets=[dataset_db])

    # Mock project retrieval by name
    project_db = ProjectDB(id=project_id, name=project_name)
    get_project_mock.return_value = Project(project=project_db)

    # Mock dataset projects list
    list_projects_mock.return_value = ListDatasetProjectsResponse(
        projects=[ProjectDB(id=project_id, name=project_name)]
    )

    # Call the function
    result = get_dataset(name=dataset_name, project_name=project_name)

    # Verify results
    assert result is not None
    assert result.name == dataset_name

    # Verify the project validation was called
    list_projects_mock.assert_called_once()


def test_get_dataset_with_both_project_params() -> None:
    """Test that providing both project_id and project_name raises an error."""
    from galileo.datasets import get_dataset

    with pytest.raises(ValueError, match="Only one of 'project_id' or 'project_name' can be provided, not both"):
        get_dataset(name="my-dataset", project_id="id-123", project_name="My Project")


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
def test_get_dataset_with_nonexistent_project(get_dataset_mock: Mock, get_project_mock: Mock) -> None:
    """Test getting a dataset with a project that doesn't exist."""
    from galileo.datasets import get_dataset

    dataset_id = "dataset-1"

    # Mock dataset retrieval
    dataset_db = DatasetDB(
        id=dataset_id,
        name="Test Dataset",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )
    get_dataset_mock.sync.return_value = dataset_db

    # Mock project not found
    get_project_mock.return_value = None

    with pytest.raises(ValueError, match="Project 'nonexistent-project' does not exist"):
        get_dataset(id=dataset_id, project_id="nonexistent-project")


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
@patch("galileo.resources.api.datasets.list_dataset_projects_datasets_dataset_id_projects_get.sync")
def test_get_dataset_not_in_project(list_projects_mock: Mock, get_dataset_mock: Mock, get_project_mock: Mock) -> None:
    """Test getting a dataset that is not used in the specified project."""
    from galileo.datasets import get_dataset
    from galileo.projects import Project
    from galileo.resources.models import ListDatasetProjectsResponse, ProjectDB

    dataset_id = "dataset-1"
    project_id = "test-project-id"
    other_project_id = "other-project-id"

    # Mock dataset retrieval
    dataset_db = DatasetDB(
        id=dataset_id,
        name="Test Dataset",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )
    get_dataset_mock.sync.return_value = dataset_db

    # Mock project retrieval
    project_db = ProjectDB(id=project_id, name="Test Project")
    get_project_mock.return_value = Project(project=project_db)

    # Mock dataset is used in a different project
    list_projects_mock.return_value = ListDatasetProjectsResponse(
        projects=[ProjectDB(id=other_project_id, name="Other Project")]
    )

    with pytest.raises(ValueError, match="Dataset 'dataset-1' is not used in project 'test-project-id'"):
        get_dataset(id=dataset_id, project_id=project_id)


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
@patch("galileo.resources.api.datasets.list_dataset_projects_datasets_dataset_id_projects_get.sync")
@patch("galileo.datasets.delete_dataset_datasets_dataset_id_delete")
def test_delete_dataset_with_project_id(
    delete_dataset_mock: Mock, list_projects_mock: Mock, get_dataset_mock: Mock, get_project_mock: Mock
) -> None:
    """Test deleting a dataset with project_id validation."""
    from galileo.datasets import delete_dataset
    from galileo.projects import Project
    from galileo.resources.models import ListDatasetProjectsResponse, ProjectDB

    dataset_id = "dataset-1"
    project_id = "test-project-id"

    # Mock dataset retrieval
    dataset_db = DatasetDB(
        id=dataset_id,
        name="Test Dataset",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )
    get_dataset_mock.sync.return_value = dataset_db

    # Mock project retrieval
    project_db = ProjectDB(id=project_id, name="Test Project")
    get_project_mock.return_value = Project(project=project_db)

    # Mock dataset projects list
    list_projects_mock.return_value = ListDatasetProjectsResponse(
        projects=[ProjectDB(id=project_id, name="Test Project")]
    )

    # Mock deletion
    delete_dataset_mock.sync.return_value = None

    # Call the function
    delete_dataset(id=dataset_id, project_id=project_id)

    # Verify deletion was called
    delete_dataset_mock.sync.assert_called_once_with(client=ANY, dataset_id=dataset_id)


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.query_datasets_datasets_query_post")
@patch("galileo.resources.api.datasets.list_dataset_projects_datasets_dataset_id_projects_get.sync")
@patch("galileo.datasets.delete_dataset_datasets_dataset_id_delete")
def test_delete_dataset_with_project_name(
    delete_dataset_mock: Mock, list_projects_mock: Mock, query_datasets_mock: Mock, get_project_mock: Mock
) -> None:
    """Test deleting a dataset with project_name validation."""
    from galileo.datasets import delete_dataset
    from galileo.projects import Project
    from galileo.resources.models import ListDatasetProjectsResponse, ProjectDB

    dataset_name = "Test Dataset"
    dataset_id = "dataset-1"
    project_name = "Test Project"
    project_id = "test-project-id"

    # Mock dataset retrieval by name
    dataset_db = DatasetDB(
        id=dataset_id,
        name=dataset_name,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )
    query_datasets_mock.sync.return_value = ListDatasetResponse(datasets=[dataset_db])

    # Mock project retrieval by name
    project_db = ProjectDB(id=project_id, name=project_name)
    get_project_mock.return_value = Project(project=project_db)

    # Mock dataset projects list
    list_projects_mock.return_value = ListDatasetProjectsResponse(
        projects=[ProjectDB(id=project_id, name=project_name)]
    )

    # Mock deletion
    delete_dataset_mock.sync.return_value = None

    # Call the function
    delete_dataset(name=dataset_name, project_name=project_name)

    # Verify deletion was called
    delete_dataset_mock.sync.assert_called_once_with(client=ANY, dataset_id=dataset_id)


def test_delete_dataset_with_both_project_params() -> None:
    """Test that providing both project_id and project_name raises an error."""
    from galileo.datasets import delete_dataset

    with pytest.raises(ValueError, match="Only one of 'project_id' or 'project_name' can be provided, not both"):
        delete_dataset(name="my-dataset", project_id="id-123", project_name="My Project")


@patch("galileo.projects.Projects.get")
@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
@patch("galileo.resources.api.datasets.list_dataset_projects_datasets_dataset_id_projects_get.sync")
def test_delete_dataset_not_in_project(
    list_projects_mock: Mock, get_dataset_mock: Mock, get_project_mock: Mock
) -> None:
    """Test deleting a dataset that is not used in the specified project."""
    from galileo.datasets import delete_dataset
    from galileo.projects import Project
    from galileo.resources.models import ListDatasetProjectsResponse, ProjectDB

    dataset_id = "dataset-1"
    project_id = "test-project-id"
    other_project_id = "other-project-id"

    # Mock dataset retrieval
    dataset_db = DatasetDB(
        id=dataset_id,
        name="Test Dataset",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        column_names=["input", "output"],
        current_version_index=0,
        draft=False,
        num_rows=10,
        project_count=1,
        created_by_user=None,
    )
    get_dataset_mock.sync.return_value = dataset_db

    # Mock project retrieval
    project_db = ProjectDB(id=project_id, name="Test Project")
    get_project_mock.return_value = Project(project=project_db)

    # Mock dataset is used in a different project
    list_projects_mock.return_value = ListDatasetProjectsResponse(
        projects=[ProjectDB(id=other_project_id, name="Other Project")]
    )

    with pytest.raises(ValueError, match="Dataset 'dataset-1' is not used in project 'test-project-id'"):
        delete_dataset(id=dataset_id, project_id=project_id)
