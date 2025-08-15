import json
from unittest.mock import patch
from uuid import uuid4

import httpx
import pytest

from galileo.export import export_records
from galileo.resources.errors import UnexpectedStatus
from galileo.resources.models import (
    LLMExportFormat,
    LogRecordsExportRequest,
    LogRecordsSortClause,
    LogRecordsTextFilter,
    RootType,
)


@patch("galileo.export.export_records_stream")
def test_export_records_basic(mock_export_records_stream):
    project_id = uuid4()
    records_data = [
        {"id": str(uuid4()), "input": "test input 1", "output": "test output 1"},
        {"id": str(uuid4()), "input": "test input 2", "output": "test output 2"},
    ]
    raw_content = b"\n".join([json.dumps(d).encode("utf-8") for d in records_data])
    mock_response = httpx.Response(200, content=raw_content)
    mock_export_records_stream.return_value = mock_response

    column_ids = ["id", "input", "output"]
    sort = LogRecordsSortClause(column_id="created_at", ascending=True)
    result = list(export_records(project_id=project_id, root_type=RootType.TRACE, column_ids=column_ids, sort=sort))

    assert len(result) == 2
    assert result[0]["input"] == "test input 1"
    mock_export_records_stream.assert_called_once()
    request_body = mock_export_records_stream.call_args.kwargs["body"]
    assert isinstance(request_body, LogRecordsExportRequest)
    assert request_body.root_type == RootType.TRACE
    assert request_body.column_ids == column_ids
    assert request_body.sort == sort


@patch("galileo.export.export_records_stream")
def test_export_records_with_log_stream_id(mock_export_records_stream):
    project_id = uuid4()
    log_stream_id = uuid4()
    mock_response = httpx.Response(200, content=b"")
    mock_export_records_stream.return_value = mock_response

    list(export_records(project_id=project_id, root_type=RootType.TRACE, log_stream_id=log_stream_id))

    mock_export_records_stream.assert_called_once()
    request_body = mock_export_records_stream.call_args.kwargs["body"]
    assert request_body.log_stream_id == log_stream_id


@patch("galileo.export.export_records_stream")
def test_export_records_with_filters(mock_export_records_stream):
    project_id = uuid4()
    filters = [LogRecordsTextFilter(column_id="input", value="test", operator="eq")]
    mock_response = httpx.Response(200, content=b"")
    mock_export_records_stream.return_value = mock_response

    list(export_records(project_id=project_id, root_type=RootType.TRACE, filters=filters))

    mock_export_records_stream.assert_called_once()
    request_body = mock_export_records_stream.call_args.kwargs["body"]
    assert request_body.filters == filters


@patch("galileo.export.export_records_stream")
def test_export_records_api_failure(mock_export_records_stream):
    project_id = uuid4()
    mock_export_records_stream.side_effect = UnexpectedStatus(400, b"Bad Request")

    with pytest.raises(UnexpectedStatus):
        list(export_records(project_id=project_id, root_type=RootType.TRACE))


@pytest.mark.parametrize("root_type", [RootType.TRACE, RootType.SPAN, RootType.SESSION])
@patch("galileo.export.export_records_stream")
def test_export_records_all_root_types(mock_export_records_stream, root_type):
    project_id = uuid4()
    mock_response = httpx.Response(200, content=b"")
    mock_export_records_stream.return_value = mock_response

    list(export_records(project_id=project_id, root_type=root_type))

    mock_export_records_stream.assert_called_once()
    request_body = mock_export_records_stream.call_args.kwargs["body"]
    assert request_body.root_type == root_type


@patch("galileo.export.export_records_stream")
def test_export_records_empty_response(mock_export_records_stream):
    project_id = uuid4()
    mock_response = httpx.Response(200, content=b"")
    mock_export_records_stream.return_value = mock_response

    result = list(export_records(project_id=project_id, root_type=RootType.TRACE))
    assert len(result) == 0


@patch("galileo.export.export_records_stream")
def test_export_records_malformed_json(mock_export_records_stream):
    project_id = uuid4()
    raw_content = b'{"id": "123", "input": "test"}\nthis is not json'
    mock_response = httpx.Response(200, content=raw_content)
    mock_export_records_stream.return_value = mock_response

    with pytest.raises(json.JSONDecodeError):
        list(export_records(project_id=project_id, root_type=RootType.TRACE))


@patch("galileo.export.export_records_stream")
def test_export_records_csv(mock_export_records_stream):
    project_id = uuid4()
    csv_content = "id,input,output\n1,test1,out1\n2,test2,out2"
    mock_response = httpx.Response(200, content=csv_content.encode("utf-8"))
    mock_export_records_stream.return_value = mock_response

    result = list(export_records(project_id=project_id, root_type=RootType.TRACE, export_format=LLMExportFormat.CSV))

    assert len(result) == 2
    assert result[0] == {"id": "1", "input": "test1", "output": "out1"}
    assert result[1] == {"id": "2", "input": "test2", "output": "out2"}
    request_body = mock_export_records_stream.call_args.kwargs["body"]
    assert request_body.export_format == LLMExportFormat.CSV
