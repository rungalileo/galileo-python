from unittest.mock import MagicMock

import pytest

from galileo.__future__.shared.query_result import QueryResult, _flatten_dict
from galileo.resources.models import LogRecordsQueryResponse
from galileo.resources.types import UNSET
from galileo.search import RecordType


@pytest.mark.parametrize(
    "input_dict,expected",
    [
        ({"a": 1}, {"a": 1}),
        ({"a": {"b": 2}}, {"a_b": 2}),
        ({"a": {"b": {"c": 3}}}, {"a_b_c": 3}),
        ({"a": 1, "b": {"c": 2, "d": 3}}, {"a": 1, "b_c": 2, "b_d": 3}),
    ],
)
def test_flatten_dict(input_dict, expected):
    """Test dictionary flattening with various nesting levels."""
    assert _flatten_dict(input_dict) == expected


@pytest.mark.parametrize("limit,expected_limit", [(10, 10), (UNSET, 100), (None, 100)])
def test_limit_property(limit, expected_limit):
    """Test limit property handles UNSET and None."""
    mock_response = MagicMock(spec=LogRecordsQueryResponse, limit=limit, records=[])
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)
    assert result.limit == expected_limit


@pytest.mark.parametrize("next_token,expected_has_next", [(10, True), (None, False), (UNSET, False)])
def test_has_next_page(next_token, expected_has_next):
    """Test has_next_page property."""
    mock_response = MagicMock(spec=LogRecordsQueryResponse, next_starting_token=next_token, records=[])
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)
    assert result.has_next_page == expected_has_next


def test_list_behavior():
    """Test list-like access: len, index, slice, iteration."""
    records = [MagicMock(to_dict=MagicMock(return_value={"id": str(i)})) for i in range(5)]
    mock_response = MagicMock(spec=LogRecordsQueryResponse, records=records)
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)

    assert len(result) == 5
    assert result[0]["id"] == "0"
    assert result[-1]["id"] == "4"
    assert len(result[:3]) == 3
    assert [r["id"] for r in result] == ["0", "1", "2", "3", "4"]


def test_flattening():
    """Test nested records are flattened."""
    record = MagicMock(
        to_dict=MagicMock(return_value={"id": "1", "metrics": {"score": {"value": 0.9}}, "meta": {"tag": "test"}})
    )
    mock_response = MagicMock(spec=LogRecordsQueryResponse, records=[record])
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)

    flat = result[0]
    assert flat["id"] == "1"
    assert flat["metrics_score_value"] == 0.9
    assert flat["meta_tag"] == "test"
    assert "metrics" not in flat


def test_next_page_success():
    """Test next_page extends current results."""
    records1 = [MagicMock(to_dict=MagicMock(return_value={"id": "1"}))]
    records2 = [MagicMock(to_dict=MagicMock(return_value={"id": "2"}))]

    mock_response = MagicMock(spec=LogRecordsQueryResponse, limit=10, next_starting_token=10, records=records1)
    mock_next_response = MagicMock(spec=LogRecordsQueryResponse, limit=10, next_starting_token=None, records=records2)
    query_fn = MagicMock(return_value=mock_next_response)
    filters, sort = [MagicMock()], MagicMock()

    result = QueryResult(mock_response, query_fn, RecordType.SPAN, filters, sort)
    assert len(result) == 1

    result.next_page()

    query_fn.assert_called_once_with(
        record_type=RecordType.SPAN, filters=filters, sort=sort, limit=10, starting_token=10
    )
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"


def test_next_page_no_next_raises():
    """Test next_page raises when no next page available."""
    mock_response = MagicMock(spec=LogRecordsQueryResponse, next_starting_token=None, records=[])
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)

    with pytest.raises(ValueError, match="No next page available"):
        result.next_page()


def test_empty_records():
    """Test QueryResult with no records."""
    mock_response = MagicMock(spec=LogRecordsQueryResponse, records=[])
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)

    assert len(result) == 0
    assert result.to_list() == []


def test_unset_records():
    """Test QueryResult with UNSET records."""
    mock_response = MagicMock(spec=LogRecordsQueryResponse, records=UNSET)
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)

    assert len(result) == 0
    assert result.to_list() == []


def test_caching():
    """Test records are flattened once and cached."""
    record = MagicMock(to_dict=MagicMock(return_value={"id": "1"}))
    mock_response = MagicMock(spec=LogRecordsQueryResponse, records=[record])
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)

    _ = result[0]
    _ = result[0]
    assert record.to_dict.call_count == 1  # Only called once


def test_to_list():
    """Test to_list returns a regular list."""
    records = [MagicMock(to_dict=MagicMock(return_value={"id": str(i)})) for i in range(3)]
    mock_response = MagicMock(spec=LogRecordsQueryResponse, records=records)
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)

    lst = result.to_list()
    assert isinstance(lst, list)
    assert len(lst) == 3
    assert lst[0]["id"] == "0"


@pytest.mark.parametrize("index,should_fail", [(0, False), (5, True), (-1, False), (-6, True)])
def test_index_access_edge_cases(index, should_fail):
    """Test index access with valid and invalid indices."""
    records = [MagicMock(to_dict=MagicMock(return_value={"id": str(i)})) for i in range(5)]
    mock_response = MagicMock(spec=LogRecordsQueryResponse, records=records)
    result = QueryResult(mock_response, MagicMock(), RecordType.SPAN, None, None)

    if should_fail:
        with pytest.raises(IndexError):
            _ = result[index]
    else:
        _ = result[index]  # Should not raise


def test_next_page_extends_results():
    """Test next_page extends the current result."""
    records1 = [MagicMock(to_dict=MagicMock(return_value={"id": str(i)})) for i in range(3)]
    records2 = [MagicMock(to_dict=MagicMock(return_value={"id": str(i)})) for i in range(3, 6)]

    mock_response1 = MagicMock(spec=LogRecordsQueryResponse, limit=3, next_starting_token=3, records=records1)
    mock_response2 = MagicMock(spec=LogRecordsQueryResponse, limit=3, next_starting_token=None, records=records2)

    query_fn = MagicMock(return_value=mock_response2)
    result = QueryResult(mock_response1, query_fn, RecordType.SPAN, None, None)

    assert len(result) == 3
    result.next_page()
    assert len(result) == 6
    assert [r["id"] for r in result] == ["0", "1", "2", "3", "4", "5"]
