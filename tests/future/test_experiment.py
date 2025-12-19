from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import Experiment
from galileo.__future__.shared.base import SyncState
from galileo.__future__.shared.column import ColumnCollection
from galileo.__future__.shared.exceptions import ValidationError
from galileo.__future__.shared.experiment_result import ExperimentRunResult, ExperimentStatusInfo
from galileo.__future__.shared.query_result import QueryResult
from galileo.resources.models import ExperimentResponse
from galileo.schema.metrics import GalileoMetrics
from galileo.search import RecordType


@pytest.fixture
def mock_experiment_response() -> MagicMock:
    """Create a mock ExperimentResponse for testing."""
    mock_response = MagicMock(spec=ExperimentResponse)
    mock_response.id = str(uuid4())
    mock_response.name = "Test Experiment"
    mock_response.created_at = datetime.now(timezone.utc)
    mock_response.updated_at = datetime.now(timezone.utc)
    mock_response.additional_properties = {}
    return mock_response


@pytest.fixture
def mock_project() -> MagicMock:
    """Create a mock Project for testing."""
    mock_proj = MagicMock()
    mock_proj.id = str(uuid4())
    mock_proj.name = "Test Project"
    return mock_proj


@pytest.fixture
def synced_experiment() -> Experiment:
    """Create a synced experiment with ID and project_id set."""
    experiment = Experiment._create_empty()
    experiment.id = str(uuid4())
    experiment.project_id = str(uuid4())
    experiment.name = "Test Experiment"
    experiment._set_state(SyncState.SYNCED)
    return experiment


@pytest.fixture
def local_experiment() -> Experiment:
    """Create a local-only experiment without ID."""
    experiment = Experiment._create_empty()
    experiment.name = "Test"
    experiment.project_name = "Test Project"
    experiment._set_state(SyncState.LOCAL_ONLY)
    return experiment


class TestExperimentInitialization:
    """Test suite for Experiment initialization."""

    @pytest.mark.parametrize("project_kwarg", [{"project_id": "test-project-id"}, {"project_name": "Test Project"}])
    def test_init_with_name_and_project(self, project_kwarg: dict, reset_configuration: None) -> None:
        """Test initializing an experiment with name and project creates a local-only instance."""
        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", **project_kwarg
        )

        assert experiment.name == "Test Experiment"
        assert experiment.id is None
        assert experiment.sync_state == SyncState.LOCAL_ONLY

        if "project_id" in project_kwarg:
            assert experiment.project_id == project_kwarg["project_id"]
            assert experiment.project_name is None
        else:
            assert experiment.project_name == project_kwarg["project_name"]
            assert experiment.project_id is None

    def test_init_with_dataset_name(self, reset_configuration: None) -> None:
        """Test initializing an experiment with dataset name."""
        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        )

        assert experiment.dataset_name == "test-dataset"
        assert experiment.dataset_id is None

    def test_init_with_prompt_name(self, reset_configuration: None) -> None:
        """Test initializing an experiment with prompt name."""
        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        )

        assert experiment.prompt_name == "test-prompt"
        assert experiment.prompt_id is None

    def test_init_with_metrics(self, reset_configuration: None) -> None:
        """Test initializing an experiment with metrics."""
        metrics = [GalileoMetrics.correctness, "completeness"]
        experiment = Experiment(
            name="Test Experiment",
            dataset_name="test-dataset",
            prompt_name="test-prompt",
            metrics=metrics,
            project_name="Test Project",
        )

        assert experiment.metrics == metrics

    def test_init_without_name_raises_validation_error(self, reset_configuration: None) -> None:
        """Test initializing an experiment without a name raises ValidationError."""
        with pytest.raises(ValidationError, match="'name' must be provided"):
            Experiment(name="", dataset_name="test-dataset", prompt_name="test-prompt", project_id="test-project-id")

    def test_init_without_project_raises_validation_error(self, reset_configuration: None) -> None:
        """Test initializing an experiment without project info raises ValidationError."""
        with pytest.raises(ValidationError):
            Experiment(name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt")

    def test_init_with_both_project_id_and_name_raises_validation_error(self, reset_configuration: None) -> None:
        """Test initializing an experiment with both project_id and project_name raises ValidationError."""
        with pytest.raises(ValidationError):
            Experiment(
                name="Test Experiment",
                dataset_name="test-dataset",
                prompt_name="test-prompt",
                project_id="test-id",
                project_name="Test Project",
            )


class TestExperimentCreate:
    """Test suite for Experiment.create() method."""

    @patch("galileo.__future__.experiment.load_dataset_and_records")
    @patch("galileo.__future__.experiment.Projects")
    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_create_persists_experiment_to_api(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test create() persists the experiment to the API and updates attributes."""
        # Setup mocks
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None  # No existing experiment
        mock_experiments_service.create.return_value = mock_experiment_response

        # Create experiment
        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        ).create()

        # Verify
        mock_experiments_service.create.assert_called_once()
        assert experiment.id == mock_experiment_response.id
        assert experiment.is_synced()
        assert experiment.project_id == mock_project.id

    @patch("galileo.__future__.experiment.load_dataset_and_records")
    @patch("galileo.__future__.experiment.Projects")
    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_create_handles_existing_experiment_with_timestamp(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test create() adds timestamp when experiment with same name exists."""
        # Setup mocks
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        existing_experiment = MagicMock()
        existing_experiment.name = "Test Experiment"

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = existing_experiment  # Existing experiment found
        mock_experiments_service.create.return_value = mock_experiment_response

        # Create experiment
        Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        ).create()

        # Verify name was changed (should have timestamp appended)
        call_args = mock_experiments_service.create.call_args
        assert "Test Experiment" in call_args.kwargs["name"]
        assert call_args.kwargs["name"] != "Test Experiment"  # Name was modified

    @patch("galileo.__future__.experiment.load_dataset_and_records")
    @patch("galileo.__future__.experiment.Projects")
    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_create_handles_api_failure(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test create() handles API failures and sets state correctly."""
        # Setup mocks
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None
        mock_experiments_service.create.side_effect = Exception("API Error")

        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_id="test-project-id"
        )

        with pytest.raises(Exception, match="API Error"):
            experiment.create()

        assert experiment.sync_state == SyncState.FAILED_SYNC


class TestExperimentGet:
    """Test suite for Experiment.get() class method."""

    @patch("galileo.__future__.experiment.Projects")
    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_get_retrieves_experiment_by_name(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test get() retrieves an existing experiment by name."""
        # Setup mocks
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = mock_experiment_response

        # Get experiment
        experiment = Experiment.get(name="Test Experiment", project_name="Test Project")

        # Verify
        assert experiment is not None
        assert experiment.id == mock_experiment_response.id
        assert experiment.name == mock_experiment_response.name
        assert experiment.is_synced()
        assert experiment.project_id == mock_project.id

    @patch("galileo.__future__.experiment.Projects")
    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_get_returns_none_when_not_found(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test get() returns None when experiment is not found."""
        # Setup mocks
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None

        # Get experiment
        experiment = Experiment.get(name="Nonexistent", project_name="Test Project")

        # Verify
        assert experiment is None


class TestExperimentList:
    """Test suite for Experiment.list() class method."""

    @patch("galileo.__future__.experiment.Projects")
    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_list_retrieves_all_experiments(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test list() retrieves all experiments for a project."""
        # Setup mocks
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_exp1 = MagicMock(spec=ExperimentResponse)
        mock_exp1.id = str(uuid4())
        mock_exp1.name = "Experiment 1"
        mock_exp1.created_at = datetime.now(timezone.utc)
        mock_exp1.updated_at = datetime.now(timezone.utc)
        mock_exp1.additional_properties = {}

        mock_exp2 = MagicMock(spec=ExperimentResponse)
        mock_exp2.id = str(uuid4())
        mock_exp2.name = "Experiment 2"
        mock_exp2.created_at = datetime.now(timezone.utc)
        mock_exp2.updated_at = datetime.now(timezone.utc)
        mock_exp2.additional_properties = {}

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.list.return_value = [mock_exp1, mock_exp2]

        # List experiments
        experiments = Experiment.list(project_name="Test Project")

        # Verify
        assert len(experiments) == 2
        assert all(exp.is_synced() for exp in experiments)
        assert all(exp.project_id == mock_project.id for exp in experiments)


class TestExperimentRun:
    """Test suite for Experiment.run() method."""

    @patch("galileo.__future__.experiment.Projects")
    @patch("galileo.__future__.experiment.ExperimentsService")
    @patch("galileo.__future__.experiment.load_dataset_and_records")
    @patch("galileo.__future__.experiment.create_metric_configs")
    def test_run_executes_prompt_template_experiment(
        self,
        mock_create_metrics: MagicMock,
        mock_load_dataset: MagicMock,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test run() executes a prompt template experiment."""
        # Setup mocks
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_dataset.dataset.id = str(uuid4())
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_create_metrics.return_value = ([], [])

        mock_prompt = MagicMock()
        mock_prompt.selected_version_id = str(uuid4())
        mock_prompt.name = "test-prompt"

        mock_exp_response = MagicMock(spec=ExperimentResponse)
        mock_exp_response.id = str(uuid4())
        mock_exp_response.name = "Test Experiment"
        mock_exp_response.project_id = mock_project.id

        result = {"link": "http://test.com", "message": "Started", "experiment": mock_exp_response}
        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.run.return_value = result

        # Create and run experiment
        experiment = Experiment._create_empty()
        experiment.name = "Test Experiment"
        experiment.id = str(uuid4())
        experiment.project_id = mock_project.id
        experiment.dataset_name = "test-dataset"
        experiment._prompt_template = mock_prompt
        experiment._experiment_response = MagicMock()
        experiment._set_state(SyncState.SYNCED)

        run_result = experiment.run()

        # Verify
        assert isinstance(run_result, ExperimentRunResult)
        assert run_result.link == result["link"]
        assert run_result.message == result["message"]
        mock_experiments_service.run.assert_called_once()

    @pytest.mark.skip(reason="Function-based experiments are temporarily disabled")
    @patch("galileo.__future__.experiment.Projects")
    @patch("galileo.__future__.experiment.ExperimentsService")
    @patch("galileo.__future__.experiment.load_dataset_and_records")
    @patch("galileo.__future__.experiment.create_metric_configs")
    def test_run_executes_function_experiment(
        self,
        mock_create_metrics: MagicMock,
        mock_load_dataset: MagicMock,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test run() executes a function-based experiment."""
        # Setup mocks
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_records = [{"input": "test"}]
        mock_load_dataset.return_value = (None, mock_records)

        mock_create_metrics.return_value = ([], [])

        mock_exp_response = MagicMock(spec=ExperimentResponse)
        mock_exp_response.id = str(uuid4())
        mock_exp_response.name = "Test Experiment"
        mock_exp_response.project_id = mock_project.id

        result = {"link": "http://test.com", "message": "Completed", "experiment": mock_exp_response}
        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.run_with_function.return_value = result

        # Create and run experiment with function
        def test_func(row):
            return "result"

        experiment = Experiment._create_empty()
        experiment.name = "Test Experiment"
        experiment.id = str(uuid4())
        experiment.project_id = mock_project.id
        experiment.dataset_name = "test-dataset"
        experiment.function = test_func
        experiment._experiment_response = mock_exp_response
        experiment._set_state(SyncState.SYNCED)

        run_result = experiment.run()

        # Verify
        assert isinstance(run_result, ExperimentRunResult)
        assert run_result.link == result["link"]
        assert run_result.message == result["message"]
        mock_experiments_service.run_with_function.assert_called_once()

    def test_run_raises_error_when_not_created(self, reset_configuration: None) -> None:
        """Test run() raises error when experiment hasn't been created."""
        experiment = Experiment(
            name="Test", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        )

        with pytest.raises(ValueError, match="Experiment must be created before running"):
            experiment.run()


class TestExperimentQuery:
    """Test suite for Experiment query methods."""

    @patch("galileo.__future__.experiment.Search")
    def test_query_returns_query_result(
        self, mock_search_class: MagicMock, synced_experiment: Experiment, reset_configuration: None
    ) -> None:
        """Test query() returns QueryResult with proper configuration."""
        mock_search_service = MagicMock()
        mock_search_class.return_value = mock_search_service
        mock_response = MagicMock()
        mock_response.records = []
        mock_response.total = 0
        mock_response.next_token = None
        mock_search_service.query.return_value = mock_response

        result = synced_experiment.query(record_type=RecordType.TRACE)

        assert isinstance(result, QueryResult)
        mock_search_service.query.assert_called_once()

    def test_query_raises_error_when_not_synced(self, reset_configuration: None) -> None:
        """Test query() raises error when experiment is local-only."""
        experiment = Experiment(
            name="Test", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        )

        with pytest.raises(ValueError, match="Experiment ID is not set"):
            experiment.query(record_type=RecordType.TRACE)


class TestExperimentRelationships:
    """Test suite for Experiment relationship properties."""

    @patch("galileo.__future__.project.Project")
    def test_project_property_returns_project(
        self,
        mock_project_class: MagicMock,
        synced_experiment: Experiment,
        mock_project: MagicMock,
        reset_configuration: None,
    ) -> None:
        """Test project property retrieves the parent project."""
        mock_project_class.get.return_value = mock_project

        synced_experiment.project_id = mock_project.id
        assert synced_experiment.project == mock_project
        mock_project_class.get.assert_called_once_with(id=mock_project.id)

    def test_relationship_properties_return_none_when_not_set(
        self, synced_experiment: Experiment, reset_configuration: None
    ) -> None:
        """Test dataset and prompt properties return None when not set."""
        synced_experiment.dataset_id = None
        synced_experiment.dataset_name = None
        synced_experiment.prompt_id = None
        synced_experiment.prompt_name = None

        assert synced_experiment.dataset is None
        assert synced_experiment.prompt is None


class TestExperimentLifecycle:
    """Test suite for Experiment lifecycle methods (refresh, delete)."""

    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_refresh_updates_attributes(
        self,
        mock_experiments_class: MagicMock,
        synced_experiment: Experiment,
        mock_experiment_response: MagicMock,
        reset_configuration: None,
    ) -> None:
        """Test refresh() updates attributes from API."""
        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = mock_experiment_response

        synced_experiment.name = "Old Name"
        synced_experiment.refresh()

        assert synced_experiment.name == mock_experiment_response.name
        assert synced_experiment.is_synced()

    @patch("galileo.__future__.experiment.GalileoPythonConfig")
    @patch("galileo.__future__.experiment.delete_experiment_projects_project_id_experiments_experiment_id_delete")
    def test_delete_removes_experiment(
        self,
        mock_delete_api: MagicMock,
        mock_config_class: MagicMock,
        synced_experiment: Experiment,
        reset_configuration: None,
    ) -> None:
        """Test delete() removes experiment and sets state to DELETED."""
        mock_config = MagicMock()
        mock_config_class.get.return_value = mock_config
        mock_delete_api.sync.return_value = None

        synced_experiment.delete()

        assert synced_experiment.is_deleted()
        mock_delete_api.sync.assert_called_once()

    @pytest.mark.parametrize(
        "method_name,error_match", [("refresh", "Experiment ID is not set"), ("delete", "Experiment ID is not set")]
    )
    def test_lifecycle_methods_require_id(
        self, method_name: str, error_match: str, local_experiment: Experiment, reset_configuration: None
    ) -> None:
        """Test lifecycle methods raise error when experiment ID is not set."""
        with pytest.raises(ValueError, match=error_match):
            getattr(local_experiment, method_name)()


class TestExperimentQueryMethods:
    """Test suite for additional Experiment query methods."""

    @pytest.mark.parametrize(
        "method_name,record_type",
        [("get_traces", RecordType.TRACE), ("get_sessions", RecordType.SESSION), ("get_spans", RecordType.SPAN)],
    )
    @patch("galileo.__future__.experiment.Search")
    def test_query_convenience_methods(
        self,
        mock_search_class: MagicMock,
        method_name: str,
        record_type: RecordType,
        synced_experiment: Experiment,
        reset_configuration: None,
    ) -> None:
        """Test query convenience methods call query with correct record type."""
        mock_search_service = MagicMock()
        mock_search_class.return_value = mock_search_service
        mock_response = MagicMock()
        mock_response.records = []
        mock_response.total = 0
        mock_response.next_token = None
        mock_search_service.query.return_value = mock_response

        result = getattr(synced_experiment, method_name)()

        assert isinstance(result, QueryResult)
        assert mock_search_service.query.call_args.kwargs["record_type"] == record_type


class TestExperimentPromptMethods:
    """Test suite for Experiment prompt-related methods."""

    @pytest.mark.parametrize(
        "kwargs,expected_attr,expected_value",
        [
            ({"prompt_name": "test-prompt"}, "prompt_name", "test-prompt"),
            ({"prompt_id": "prompt-123"}, "prompt_id", "prompt-123"),
        ],
    )
    def test_set_prompt(
        self,
        kwargs: dict,
        expected_attr: str,
        expected_value: str,
        synced_experiment: Experiment,
        reset_configuration: None,
    ) -> None:
        """Test set_prompt() with different parameters."""
        synced_experiment.set_prompt(**kwargs)
        assert getattr(synced_experiment, expected_attr) == expected_value

    @patch("galileo.__future__.experiment.get_prompt")
    def test_get_prompt_template_settings(
        self, mock_get_prompt: MagicMock, synced_experiment: Experiment, reset_configuration: None
    ) -> None:
        """Test get_prompt_template_settings() with and without prompt."""
        # Test with prompt - returns settings
        mock_prompt = MagicMock()
        mock_settings = MagicMock()
        mock_prompt.selected_version.settings = mock_settings
        mock_get_prompt.return_value = mock_prompt

        synced_experiment.prompt_id = "prompt-123"
        assert synced_experiment.get_prompt_template_settings() == mock_settings

        # Test without prompt - returns None
        synced_experiment.prompt_id = None
        synced_experiment._prompt_template = None
        assert synced_experiment.get_prompt_template_settings() is None


class TestExperimentStatusMethods:
    """Test suite for Experiment status methods."""

    @pytest.mark.parametrize("has_records,expected_result", [(True, True), (False, False)])
    @patch("galileo.__future__.experiment.Search")
    def test_has_traces(
        self,
        mock_search_class: MagicMock,
        has_records: bool,
        expected_result: bool,
        synced_experiment: Experiment,
        reset_configuration: None,
    ) -> None:
        """Test has_traces() returns correct boolean based on trace existence."""
        mock_search_service = MagicMock()
        mock_search_class.return_value = mock_search_service
        mock_response = MagicMock()
        mock_response.records = [MagicMock()] if has_records else []
        mock_response.total = 1 if has_records else 0
        mock_response.next_token = None
        mock_search_service.query.return_value = mock_response

        assert synced_experiment.has_traces() is expected_result

    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_get_status_returns_status_info(
        self,
        mock_experiments_class: MagicMock,
        synced_experiment: Experiment,
        mock_experiment_response: MagicMock,
        reset_configuration: None,
    ) -> None:
        """Test get_status() returns ExperimentStatusInfo."""
        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = mock_experiment_response

        synced_experiment._experiment_response = mock_experiment_response
        status = synced_experiment.get_status()

        assert isinstance(status, ExperimentStatusInfo)


class TestExperimentProperties:
    """Test suite for Experiment computed properties."""

    def test_experiment_properties_with_response(
        self, synced_experiment: Experiment, reset_configuration: None
    ) -> None:
        """Test all experiment properties when response data is available."""
        # Setup mock response with all properties
        mock_response = MagicMock()
        mock_response.aggregate_metrics.to_dict.return_value = {"average_cost": 0.05, "total_responses": 100}
        mock_response.rank = 1
        mock_response.ranking_score = 0.95
        mock_response.winner = True
        mock_response.prompt_model = "GPT-4o"
        mock_response.tags.to_dict.return_value = {"generic": [{"key": "env", "value": "prod"}]}

        mock_playground = MagicMock()
        mock_playground.name = "test-playground"
        mock_response.playground = mock_playground

        synced_experiment._experiment_response = mock_response

        # Assert all properties
        assert synced_experiment.aggregate_metrics == {"average_cost": 0.05, "total_responses": 100}
        assert synced_experiment.rank == 1
        assert synced_experiment.ranking_score == 0.95
        assert synced_experiment.is_winner is True
        assert synced_experiment.prompt_model == "GPT-4o"
        assert synced_experiment.playground_name == "test-playground"
        assert synced_experiment.tags == {"generic": [{"key": "env", "value": "prod"}]}

    def test_experiment_properties_without_response(
        self, synced_experiment: Experiment, reset_configuration: None
    ) -> None:
        """Test all experiment properties return None when no response data."""
        synced_experiment._experiment_response = None

        assert synced_experiment.aggregate_metrics is None
        assert synced_experiment.rank is None
        assert synced_experiment.ranking_score is None
        assert synced_experiment.is_winner is False
        assert synced_experiment.prompt_model is None
        assert synced_experiment.playground_name is None
        assert synced_experiment.tags is None


class TestExperimentTagging:
    """Test suite for Experiment tagging functionality."""

    @patch("galileo.__future__.experiment.upsert_experiment_tag")
    @patch("galileo.__future__.experiment.ExperimentsService")
    def test_add_tag_upserts_tag(
        self,
        mock_experiments_class: MagicMock,
        mock_upsert_tag: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
    ) -> None:
        """Test add_tag() upserts tag via API."""
        # Store the IDs before refresh
        exp_id = str(uuid4())
        proj_id = str(uuid4())

        # Configure the mock experiment response to have the same IDs
        mock_experiment_response.id = exp_id
        mock_experiment_response.name = "Test"

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = mock_experiment_response

        experiment = Experiment._create_empty()
        experiment.id = exp_id
        experiment.project_id = proj_id
        experiment.name = "Test"
        experiment._set_state(SyncState.SYNCED)

        experiment.add_tag("environment", "production")

        mock_upsert_tag.assert_called_once_with(proj_id, exp_id, "environment", "production", "generic")

    def test_add_tag_raises_error_when_not_created(self, reset_configuration: None) -> None:
        """Test add_tag() raises error when experiment not created."""
        experiment = Experiment._create_empty()
        experiment.name = "Test"
        experiment.project_name = "Test Project"
        experiment._set_state(SyncState.LOCAL_ONLY)

        with pytest.raises(ValueError, match="Experiment must be created"):
            experiment.add_tag("key", "value")


class TestExperimentColumns:
    """Test suite for Experiment column properties."""

    @pytest.mark.parametrize(
        "property_name,api_function",
        [
            ("span_columns", "spans_available_columns_projects_project_id_spans_available_columns_post"),
            ("trace_columns", "traces_available_columns_projects_project_id_traces_available_columns_post"),
            ("session_columns", "sessions_available_columns_projects_project_id_sessions_available_columns_post"),
        ],
    )
    @patch("galileo.__future__.experiment.GalileoPythonConfig")
    def test_column_properties_return_collection(
        self,
        mock_config_class: MagicMock,
        property_name: str,
        api_function: str,
        synced_experiment: Experiment,
        reset_configuration: None,
    ) -> None:
        """Test all column properties return ColumnCollection."""
        mock_config = MagicMock()
        mock_config_class.get.return_value = mock_config

        # Patch the specific API function
        with patch(f"galileo.__future__.experiment.{api_function}") as mock_api:
            mock_response = MagicMock()
            mock_response.columns = []
            mock_api.sync.return_value = mock_response

            columns = getattr(synced_experiment, property_name)

            assert isinstance(columns, ColumnCollection)


class TestExperimentStringRepresentation:
    """Test suite for Experiment string representations."""

    def test_str_returns_readable_string(self, reset_configuration: None) -> None:
        """Test __str__() returns a readable string."""
        experiment = Experiment._create_empty()
        experiment.name = "Test Experiment"
        experiment.id = "test-id"
        experiment.project_id = "project-id"

        result = str(experiment)

        assert "Test Experiment" in result
        assert "test-id" in result
        assert "project-id" in result

    def test_repr_returns_detailed_string(self, reset_configuration: None) -> None:
        """Test __repr__() returns a detailed string."""
        experiment = Experiment._create_empty()
        experiment.name = "Test Experiment"
        experiment.id = "test-id"
        experiment.project_id = "project-id"
        experiment.created_at = datetime.now(timezone.utc)

        result = repr(experiment)

        assert "Test Experiment" in result
        assert "test-id" in result
        assert "created_at" in result
