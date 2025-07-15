import json
from unittest.mock import patch
from uuid import uuid4

import httpx
import pytest

from galileo.export import export_records
from galileo.resources.errors import UnexpectedStatus
from galileo.resources.models import LogRecordsExportRequest, LogRecordsTextFilter, RootType
from galileo.resources.types import Response


@patch("galileo.export.export_records_sync")
def test_export_records_basic(mock_export_records_sync):
    project_id = uuid4()
    records_data = [
        {"id": str(uuid4()), "input": "test input 1", "output": "test output 1"},
        {"id": str(uuid4()), "input": "test input 2", "output": "test output 2"},
    ]
    raw_content = b"\n".join([json.dumps(d).encode("utf-8") for d in records_data])
    mock_response = httpx.Response(200, content=raw_content)
    mock_export_records_sync.return_value = Response(status_code=200, content=mock_response, headers={}, parsed=None)

    result = list(export_records(project_id=project_id, root_type=RootType.TRACE))

    assert len(result) == 2
    assert result[0]["input"] == "test input 1"
    mock_export_records_sync.assert_called_once()
    request_body = mock_export_records_sync.call_args.kwargs["body"]
    assert isinstance(request_body, LogRecordsExportRequest)
    assert request_body.root_type == RootType.TRACE


@patch("galileo.export.export_records_sync")
def test_export_records_with_log_stream_id(mock_export_records_sync):
    project_id = uuid4()
    log_stream_id = uuid4()
    mock_response = httpx.Response(200, content=b"")
    mock_export_records_sync.return_value = Response(status_code=200, content=mock_response, headers={}, parsed=None)

    list(export_records(project_id=project_id, root_type=RootType.TRACE, log_stream_id=log_stream_id))

    mock_export_records_sync.assert_called_once()
    request_body = mock_export_records_sync.call_args.kwargs["body"]
    assert request_body.log_stream_id == log_stream_id


@patch("galileo.export.export_records_sync")
def test_export_records_with_filters(mock_export_records_sync):
    project_id = uuid4()
    filters = [LogRecordsTextFilter(column_id="input", value="test", operator="eq")]
    mock_response = httpx.Response(200, content=b"")
    mock_export_records_sync.return_value = Response(status_code=200, content=mock_response, headers={}, parsed=None)

    list(export_records(project_id=project_id, root_type=RootType.TRACE, filters=filters))

    mock_export_records_sync.assert_called_once()
    request_body = mock_export_records_sync.call_args.kwargs["body"]
    assert request_body.filters == filters


@patch("galileo.export.export_records_sync")
def test_export_records_api_failure(mock_export_records_sync):
    project_id = uuid4()
    mock_export_records_sync.side_effect = UnexpectedStatus(400, b"Bad Request")

    with pytest.raises(UnexpectedStatus):
        list(export_records(project_id=project_id, root_type=RootType.TRACE))
