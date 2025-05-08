import json

import pytest

from galileo.schema.datasets import DatasetRecord


class TestDatasetRecordValidators:
    def test_validate_input(self):
        # Test with string input
        record = DatasetRecord(input="test input")
        assert record.input == "test input"

        # Test with dict input (should be converted to JSON string)
        test_dict = {"key": "value"}
        record = DatasetRecord(input=test_dict)
        assert record.input == json.dumps(test_dict)

        # Test with list input (should be converted to JSON string)
        test_list = [1, 2, 3]
        record = DatasetRecord(input=test_list)
        assert record.input == json.dumps(test_list)

        # Test with number input (should be converted to JSON string)
        record = DatasetRecord(input=42)
        assert record.input == json.dumps(42)

    def test_validate_output(self):
        # Test with None output
        record = DatasetRecord(input="test", output=None)
        assert record.output is None

        # Test with string output
        record = DatasetRecord(input="test", output="test output")
        assert record.output == "test output"

        # Test with dict output (should be converted to JSON string)
        test_dict = {"key": "value"}
        record = DatasetRecord(input="test", output=test_dict)
        assert record.output == json.dumps(test_dict)

        # Test with list output (should be converted to JSON string)
        test_list = [1, 2, 3]
        record = DatasetRecord(input="test", output=test_list)
        assert record.output == json.dumps(test_list)

    def test_validate_metadata(self):
        # Test with None metadata
        record = DatasetRecord(input="test", metadata=None)
        assert record.metadata is None

        # Test with dict metadata
        test_dict = {"key": "value"}
        record = DatasetRecord(input="test", metadata=test_dict)
        assert record.metadata == test_dict

        # Test with JSON string metadata
        json_str = '{"key": "value"}'
        record = DatasetRecord(input="test", metadata=json_str)
        assert record.metadata == {"key": "value"}

        # Test with simple string metadata (should be wrapped in a dict)
        record = DatasetRecord(input="test", metadata="metadata value")
        assert record.metadata == {"metadata": "metadata value"}

        # Test with invalid metadata type
        with pytest.raises(Exception, match="1 validation error for DatasetRecord"):
            DatasetRecord(input="test", metadata=[1, 2, 3])

        # Test with metadata containing non-string values
        with pytest.raises(Exception, match="1 validation error for DatasetRecord"):
            DatasetRecord(input="test", metadata={"key": 123})


class TestDatasetRecordDeserializedProperties:
    def test_deserialized_input(self):
        # Test with JSON string input
        test_dict = {"key": "value"}
        record = DatasetRecord(input=json.dumps(test_dict))
        assert record.deserialized_input == test_dict

        # Test with non-JSON string input
        record = DatasetRecord(input="plain text")
        assert record.deserialized_input == "plain text"

        # Test with complex nested JSON
        complex_json = {"nested": {"array": [1, 2, 3], "object": {"key": "value"}}}
        record = DatasetRecord(input=json.dumps(complex_json))
        assert record.deserialized_input == complex_json

    def test_deserialized_output(self):
        # Test with None output
        record = DatasetRecord(input="test", output=None)
        assert record.deserialized_output is None

        # Test with JSON string output
        test_dict = {"key": "value"}
        record = DatasetRecord(input="test", output=json.dumps(test_dict))
        assert record.deserialized_output == test_dict

        # Test with non-JSON string output
        record = DatasetRecord(input="test", output="plain text")
        assert record.deserialized_output == "plain text"

        # Test with complex nested JSON
        complex_json = {"nested": {"array": [1, 2, 3], "object": {"key": "value"}}}
        record = DatasetRecord(input="test", output=json.dumps(complex_json))
        assert record.deserialized_output == complex_json
