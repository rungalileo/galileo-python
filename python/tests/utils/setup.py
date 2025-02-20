from unittest.mock import AsyncMock, Mock
import datetime
from uuid import UUID
from galileo.projects import Project
from galileo.log_streams import LogStream
from galileo.resources.models.project_create_response import ProjectCreateResponse
from galileo.resources.models.log_stream_response import LogStreamResponse


def setup_mock_projects_client(mock_projects_client: Mock):
    now = datetime.datetime.now()
    mock_instance = mock_projects_client.return_value
    mock_get_project_by_name = Mock(
        return_value=Project(
            ProjectCreateResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                type_="gen_ai",
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_create_project = Mock(
        return_value=Project(
            ProjectCreateResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                type_="gen_ai",
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_instance.get = mock_get_project_by_name
    mock_instance.create = mock_create_project
    return mock_instance


def setup_mock_logstreams_client(mock_logstreams_client: Mock):
    now = datetime.datetime.now()
    mock_instance = mock_logstreams_client.return_value
    mock_get_logstream_by_name = Mock(
        return_value=LogStream(
            LogStreamResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                project_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_create_logstream = Mock(
        return_value=LogStream(
            LogStreamResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                project_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                name="test",
                created_at=now,
                updated_at=now,
                # additional_properties={},
            )
        )
    )
    mock_instance.get = mock_get_logstream_by_name
    mock_instance.create = mock_create_logstream
    return mock_instance


def setup_mock_core_api_client(mock_core_api_client: Mock):
    mock_instance = mock_core_api_client.return_value
    mock_ingest_traces_sync = AsyncMock(return_value={})
    mock_ingest_traces_async = AsyncMock(return_value={})
    mock_instance.get_project_by_name = AsyncMock(
        return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")}
    )
    mock_instance.get_log_stream_by_name = AsyncMock(
        return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b")}
    )
    mock_instance.ingest_traces_sync = mock_ingest_traces_sync
    mock_instance.ingest_traces = mock_ingest_traces_async
    return mock_instance
