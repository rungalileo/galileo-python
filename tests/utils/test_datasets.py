from unittest.mock import Mock, patch

import pytest

from galileo.resources.models.dataset_content import DatasetContent
from galileo.resources.models.dataset_row import DatasetRow
from galileo.resources.models.dataset_row_values_dict import DatasetRowValuesDict
from galileo.schema.datasets import DatasetRecord
from galileo.utils.datasets import (
    create_rows_from_records,
    get_dataset_and_records,
    get_records_for_dataset,
    load_dataset_and_records,
    remap_output_to_ground_truth,
)


@patch("galileo.datasets.get_dataset")
@patch("galileo.utils.datasets.get_records_for_dataset", return_value=[])
def test_get_dataset_and_records_with_id(mock_get_records, mock_get_dataset, dataset_content) -> None:
    """Test _get_dataset_and_records function with dataset_id."""
    # Setup
    mock_dataset = Mock()
    mock_dataset.get_content.return_value = dataset_content
    mock_get_dataset.return_value = mock_dataset

    # Execute
    dataset, records = get_dataset_and_records(id="test-id")

    # Assert
    mock_get_dataset.assert_called_once_with(id="test-id")
    assert dataset == mock_dataset
    mock_get_records.assert_called_once_with(mock_dataset)


@patch("galileo.datasets.get_dataset")
@patch("galileo.utils.datasets.get_records_for_dataset", return_value=[])
def test_get_dataset_and_records_with_name(mock_get_records, mock_get_dataset, dataset_content) -> None:
    """Test _get_dataset_and_records function with dataset_name."""
    # Setup
    mock_dataset = Mock()
    mock_dataset.get_content.return_value = dataset_content
    mock_get_dataset.return_value = mock_dataset

    # Execute
    dataset, records = get_dataset_and_records(name="test-dataset")

    # Assert
    mock_get_dataset.assert_called_once_with(name="test-dataset")
    assert dataset == mock_dataset
    mock_get_records.assert_called_once_with(mock_dataset)


@patch("galileo.datasets.get_dataset")
def test_get_dataset_and_records_not_found_id(mock_get_dataset) -> None:
    """Test _get_dataset_and_records function when dataset with id is not found."""
    # Setup
    mock_get_dataset.return_value = None

    # Execute and Assert
    with pytest.raises(ValueError, match="Could not find dataset with id test-id"):
        get_dataset_and_records(id="test-id")


@patch("galileo.datasets.get_dataset")
def test_get_dataset_and_records_not_found_name(mock_get_dataset) -> None:
    """Test _get_dataset_and_records function when dataset with name is not found."""
    # Setup
    mock_get_dataset.return_value = None

    # Execute and Assert
    with pytest.raises(ValueError, match="Could not find dataset with name test-dataset"):
        get_dataset_and_records(name="test-dataset")


def test_get_dataset_and_records_no_params() -> None:
    """Test _get_dataset_and_records function when no parameters are provided."""
    # Execute and Assert
    with pytest.raises(ValueError, match="Either the dataset id or name must be provided"):
        get_dataset_and_records()


@patch("galileo.datasets.convert_dataset_row_to_record")
def test_get_records_for_dataset(mock_convert, dataset_content) -> None:
    """Test _get_records_for_dataset function."""
    # Setup
    mock_dataset = Mock()
    mock_dataset.get_content.return_value = dataset_content
    mock_convert.return_value = DatasetRecord(input="test")

    # Execute
    records = get_records_for_dataset(mock_dataset)

    # Assert
    mock_dataset.get_content.assert_called_once()
    mock_convert.assert_called_once_with(dataset_content.rows[0])
    assert len(records) == 1
    assert records[0].input == "test"


def test_get_records_for_dataset_no_content() -> None:
    """Test _get_records_for_dataset function when dataset has no content."""
    # Setup
    mock_dataset = Mock()
    mock_dataset.get_content.return_value = None

    # Execute and Assert
    with pytest.raises(ValueError, match="dataset has no content"):
        get_records_for_dataset(mock_dataset)


@patch("galileo.utils.datasets.DatasetRecord")
def test_create_rows_from_records_with_input_field(mock_dataset_record) -> None:
    """Test create_rows_from_records function with records containing 'input' field."""
    # Setup
    records = [{"input": "test input", "output": "test output"}]
    mock_dataset_record.return_value = "record instance"

    # Execute
    result = create_rows_from_records(records)

    # Assert
    mock_dataset_record.assert_called_once_with(**records[0])
    assert result == ["record instance"]


@patch("galileo.utils.datasets.DatasetRecord")
def test_create_rows_from_records_without_input_field(mock_dataset_record) -> None:
    """Test create_rows_from_records function with records not containing 'input' field."""
    # Setup
    records = ["test input"]
    mock_dataset_record.return_value = "record instance"

    # Execute
    result = create_rows_from_records(records)

    # Assert
    mock_dataset_record.assert_called_once_with(input="test input")
    assert result == ["record instance"]


@patch("galileo.utils.datasets.DatasetRecord")
def test_create_rows_from_records_with_dict_without_input_field(mock_dataset_record) -> None:
    """Test create_rows_from_records function with dict records not containing 'input' field."""
    # Setup
    records = [{"key": "value"}]
    mock_dataset_record.return_value = "record instance"

    # Execute
    result = create_rows_from_records(records)

    # Assert
    mock_dataset_record.assert_called_once_with(input={"key": "value"})
    assert result == ["record instance"]


@patch("galileo.utils.datasets.DatasetRecord")
def test_create_rows_from_records_mixed_types(mock_dataset_record) -> None:
    """Test create_rows_from_records function with mixed record types."""
    # Setup
    records = [{"input": "test input 1", "output": "test output 1"}, "test input 2", {"key": "value"}]
    mock_dataset_record.side_effect = ["record 1", "record 2", "record 3"]

    # Execute
    result = create_rows_from_records(records)

    # Assert
    assert mock_dataset_record.call_count == 3
    mock_dataset_record.assert_any_call(**records[0])
    mock_dataset_record.assert_any_call(input="test input 2")
    mock_dataset_record.assert_any_call(input={"key": "value"})
    assert result == ["record 1", "record 2", "record 3"]


@patch("galileo.utils.datasets.get_dataset_and_records")
def test_load_dataset_and_records_with_dataset_id(mock_get_dataset_and_records) -> None:
    """Test load_dataset_and_records function with dataset_id."""
    # Setup
    mock_dataset = Mock()
    mock_records = [DatasetRecord(input="test")]
    mock_get_dataset_and_records.return_value = (mock_dataset, mock_records)

    # Execute
    dataset, records = load_dataset_and_records(None, "test-id", None)

    # Assert
    mock_get_dataset_and_records.assert_called_once_with(id="test-id")
    assert dataset == mock_dataset
    assert records == mock_records


@patch("galileo.utils.datasets.get_dataset_and_records")
def test_load_dataset_and_records_with_dataset_name(mock_get_dataset_and_records) -> None:
    """Test load_dataset_and_records function with dataset_name."""
    # Setup
    mock_dataset = Mock()
    mock_records = [DatasetRecord(input="test")]
    mock_get_dataset_and_records.return_value = (mock_dataset, mock_records)

    # Execute
    dataset, records = load_dataset_and_records(None, None, "test-dataset")

    # Assert
    mock_get_dataset_and_records.assert_called_once_with(name="test-dataset")
    assert dataset == mock_dataset
    assert records == mock_records


@patch("galileo.utils.datasets.get_dataset_and_records")
def test_load_dataset_and_records_with_dataset_as_string(mock_get_dataset_and_records) -> None:
    """Test load_dataset_and_records function with dataset as string."""
    # Setup
    mock_dataset = Mock()
    mock_records = [DatasetRecord(input="test")]
    mock_get_dataset_and_records.return_value = (mock_dataset, mock_records)

    # Execute
    dataset, records = load_dataset_and_records("test-dataset", None, None)

    # Assert
    mock_get_dataset_and_records.assert_called_once_with(name="test-dataset")
    assert dataset == mock_dataset
    assert records == mock_records


@patch("galileo.utils.datasets.get_records_for_dataset")
def test_load_dataset_and_records_with_dataset_object(mock_get_records) -> None:
    """Test load_dataset_and_records function with Dataset object."""
    # Setup
    from galileo.datasets import Dataset

    mock_dataset = Mock(spec=Dataset)
    mock_records = [DatasetRecord(input="test")]
    mock_get_records.return_value = mock_records

    # Execute
    dataset, records = load_dataset_and_records(mock_dataset, None, None)

    # Assert
    mock_get_records.assert_called_once_with(mock_dataset)
    assert dataset == mock_dataset
    assert records == mock_records


@patch("galileo.utils.datasets.create_rows_from_records")
def test_load_dataset_and_records_with_records_list(mockcreate_rows) -> None:
    """Test load_dataset_and_records function with list of records."""
    # Setup
    records_list = [{"input": "test input"}]
    mock_records = [DatasetRecord(input="test")]
    mockcreate_rows.return_value = mock_records

    # Execute
    dataset, records = load_dataset_and_records(records_list, None, None)

    # Assert
    mockcreate_rows.assert_called_once_with(records_list)
    assert dataset is None
    assert records == mock_records


def test_remap_output_to_ground_truth_column_names() -> None:
    """Test that remap_output_to_ground_truth renames 'output' in column_names."""
    # Given: content with 'output' in column_names
    content = DatasetContent(column_names=["input", "output", "generated_output", "metadata"], rows=[])

    # When: remapping
    result = remap_output_to_ground_truth(content)

    # Then: 'output' is renamed to 'ground_truth', other columns unchanged
    assert result.column_names == ["input", "ground_truth", "generated_output", "metadata"]


def test_remap_output_to_ground_truth_row_values() -> None:
    """Test that remap_output_to_ground_truth renames 'output' in row values_dict."""
    # Given: a row with 'output' in values_dict
    row = DatasetRow(
        index=0,
        values=["q", "a"],
        metadata=None,
        row_id="r1",
        values_dict=DatasetRowValuesDict.from_dict({"input": "q", "output": "a"}),
    )
    content = DatasetContent(column_names=["input", "output"], rows=[row])

    # When: remapping
    remap_output_to_ground_truth(content)

    # Then: row values_dict has 'ground_truth', not 'output'
    props = row.values_dict.additional_properties
    assert props.get("ground_truth") == "a"
    assert "output" not in props


def test_remap_output_to_ground_truth_no_output_column() -> None:
    """Test that remap_output_to_ground_truth leaves content unchanged when no 'output' column."""
    # Given: content with no 'output' column
    content = DatasetContent(column_names=["input", "ground_truth", "metadata"], rows=[])

    # When: remapping
    result = remap_output_to_ground_truth(content)

    # Then: column_names are unchanged
    assert result.column_names == ["input", "ground_truth", "metadata"]


def test_remap_output_to_ground_truth_row_not_renamed_without_output_column() -> None:
    """Test that row values are not renamed when column_names does not contain 'output'."""
    # Given: column_names has no 'output', but a row's values_dict does
    row = DatasetRow(
        index=0,
        values=["q", "a"],
        metadata=None,
        row_id="r1",
        values_dict=DatasetRowValuesDict.from_dict({"input": "q", "output": "a"}),
    )
    content = DatasetContent(column_names=["input", "ground_truth"], rows=[row])

    # When: remapping
    remap_output_to_ground_truth(content)

    # Then: row values_dict is left unchanged because column_names had no 'output'
    props = row.values_dict.additional_properties
    assert props.get("output") == "a"
    assert "ground_truth" not in props


def test_remap_output_to_ground_truth_row_renamed_when_column_names_unset() -> None:
    """Test that row values are renamed when column_names is Unset (e.g. paginated response)."""
    # Given: column_names is Unset but a row's values_dict contains 'output'
    row = DatasetRow(
        index=0,
        values=["q", "a"],
        metadata=None,
        row_id="r1",
        values_dict=DatasetRowValuesDict.from_dict({"input": "q", "output": "a"}),
    )
    content = DatasetContent(rows=[row])  # column_names defaults to UNSET

    # When: remapping
    remap_output_to_ground_truth(content)

    # Then: row values_dict is remapped even without column_names
    props = row.values_dict.additional_properties
    assert props.get("ground_truth") == "a"
    assert "output" not in props


def test_load_dataset_and_records_no_params() -> None:
    """Test load_dataset_and_records function when no parameters are provided."""
    # Execute and Assert
    with pytest.raises(
        ValueError, match="To load dataset records, dataset, dataset_name, or dataset_id must be provided"
    ):
        load_dataset_and_records(None, None, None)
