import datetime
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from galileo.experiments import Experiments
from galileo.log_streams import LogStream
from galileo.projects import Project
from galileo.resources.models import ExperimentResponse, ProjectType
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.resources.models.project_create_response import ProjectCreateResponse


def setup_mock_projects_client(mock_projects_client: Mock):
    now = datetime.datetime.now()
    mock_instance = mock_projects_client.return_value
    mock_instance.get = Mock(
        return_value=Project(
            ProjectCreateResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                type_=ProjectType.gen_ai,
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_instance.create = Mock(
        return_value=Project(
            ProjectCreateResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                type_=ProjectType.gen_ai,
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    return mock_instance


def setup_mock_logstreams_client(mock_logstreams_client: Mock):
    now = datetime.datetime.now()
    mock_instance = mock_logstreams_client.return_value
    mock_instance.get = Mock(
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
    mock_instance.create = Mock(
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
    return mock_instance


def setup_mock_experiments_client(mock_experiment_client: Mock):
    now = datetime.datetime.now()
    mock_instance = mock_experiment_client.return_value
    mock_instance.get = Mock(
        return_value=Experiments(
            ExperimentResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                project_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    return mock_instance


def setup_mock_core_api_client(mock_core_api_client: Mock):
    mock_instance = mock_core_api_client.return_value
    mock_instance.get_project_by_name = AsyncMock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")})
    mock_instance.get_log_stream_by_name = AsyncMock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b")})
    mock_instance.ingest_traces_sync = AsyncMock(return_value={})
    mock_instance.ingest_traces = AsyncMock(return_value={})
    return mock_instance
