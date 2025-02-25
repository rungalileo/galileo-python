import datetime
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from galileo.log_streams import LogStream
from galileo.projects import Project
from galileo.resources.models import ProjectType
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.resources.models.project_create_response import ProjectCreateResponse


def setup_mock_projects_client(mock_projects_client: Mock, project_id: str = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a"):
    now = datetime.datetime.now()
    mock_instance = mock_projects_client.return_value
    mock_get_project_by_name = Mock(
        return_value=Project(
            ProjectCreateResponse(
                id=project_id,
                type_=ProjectType.GEN_AI,
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_create_project = Mock(
        return_value=Project(
            ProjectCreateResponse(
                id=project_id,
                type_=ProjectType.GEN_AI,
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_instance.get = mock_get_project_by_name
    mock_instance.create = mock_create_project
    return mock_instance


def setup_mock_logstreams_client(mock_logstreams_client: Mock, project_id: str = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a"):
    now = datetime.datetime.now()
    mock_instance = mock_logstreams_client.return_value
    mock_get_logstream_by_name = Mock(
        return_value=LogStream(
            LogStreamResponse(
                id=project_id,
                project_id=project_id,
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_create_logstream = Mock(
        return_value=LogStream(
            LogStreamResponse(
                id=project_id,
                project_id=project_id,
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_instance.get = mock_get_logstream_by_name
    mock_instance.create = mock_create_logstream
    return mock_instance


def setup_mock_core_api_client(mock_core_api_client: Mock, project_id: str = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a"):
    mock_instance = mock_core_api_client.return_value
    mock_ingest_traces_sync = AsyncMock(return_value={})
    mock_ingest_traces_async = AsyncMock(return_value={})
    mock_instance.get_project_by_name = AsyncMock(return_value={"id": UUID(project_id)})
    mock_instance.get_log_stream_by_name = AsyncMock(return_value={"id": UUID(project_id)})
    mock_instance.ingest_traces_sync = mock_ingest_traces_sync
    mock_instance.ingest_traces = mock_ingest_traces_async
    return mock_instance
