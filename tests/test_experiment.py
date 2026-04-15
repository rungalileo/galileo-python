from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.exceptions import NotFoundError
from galileo.experiment import Experiment
from galileo.resources.models import ExperimentResponse, PromptRunSettings
from galileo.schema.metrics import GalileoMetrics
from galileo.search import RecordType
from galileo.shared.base import SyncState
from galileo.shared.column import ColumnCollection
from galileo.shared.exceptions import ResourceNotFoundError, ValidationError
from galileo.shared.experiment_result import ExperimentRunResult, ExperimentStatusInfo
from galileo.shared.query_result import QueryResult


@pytest.fixture
def mock_experiment_response() -> MagicMock:
    """Create a mock ExperimentResponse for testing."""
    mock_response = MagicMock(spec=ExperimentResponse)
    mock_response.id = str(uuid4())
    mock_response.name = "Test Experiment"
    mock_response.created_at = datetime.now(timezone.utc)
    mock_response.updated_at = datetime.now(timezone.utc)
    mock_response.additional_properties = {}
    mock_response.dataset = None
    mock_response.prompt = None
    mock_response.prompt_run_settings = None
    mock_response.prompt_model = None
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

    def test_init_without_project_succeeds(self, reset_configuration: None) -> None:
        """Test initializing an experiment without project info succeeds (validated at create time)."""
        # Given: no project_id or project_name provided
        # When: creating an experiment
        experiment = Experiment(name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt")

        # Then: experiment is created with LOCAL_ONLY state, project info is None
        assert experiment.project_id is None
        assert experiment.project_name is None
        assert experiment.sync_state == SyncState.LOCAL_ONLY

    def test_init_with_both_project_id_and_name_succeeds(self, reset_configuration: None) -> None:
        """Test initializing an experiment with both project_id and project_name succeeds (prefer id)."""
        # Given: both project_id and project_name provided
        # When: creating an experiment
        experiment = Experiment(
            name="Test Experiment",
            dataset_name="test-dataset",
            prompt_name="test-prompt",
            project_id="test-id",
            project_name="Test Project",
        )

        # Then: experiment is created with both values stored
        assert experiment.project_id == "test-id"
        assert experiment.project_name == "Test Project"


class TestExperimentEnvFallback:
    """Test suite for Experiment environment variable fallback behavior."""

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_create_uses_env_fallback_when_no_project_specified(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test create() uses Projects().get_with_env_fallbacks() when no project is specified."""
        # Given: env fallback resolves to a project
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_get_prompt.return_value = MagicMock()
        mock_create_metrics.return_value = (None, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None
        mock_experiments_service.create.return_value = mock_experiment_response

        # When: creating experiment without project params
        experiment = Experiment(name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt").create()

        # Then: project is resolved from env fallbacks
        mock_projects_service.get_with_env_fallbacks.assert_called_once()
        assert experiment.project_id == mock_project.id
        assert experiment.is_synced()

    @patch("galileo.experiment.Projects")
    def test_create_raises_error_when_no_project_and_no_env_fallback(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test create() raises ValueError when no project and no env fallback."""
        # Given: env fallback returns None (no project found)
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = None

        # When/Then: creating experiment raises ResourceNotFoundError with helpful message
        experiment = Experiment(name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt")
        with pytest.raises(ResourceNotFoundError, match="Project not found"):
            experiment.create()

    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_get_uses_env_fallback_when_no_project_specified(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test get() uses Projects().get_with_env_fallbacks() when no project is specified."""
        # Given: env fallback resolves to a project
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = mock_experiment_response

        # When: calling get() without project params
        experiment = Experiment.get(name="Test Experiment")

        # Then: project is resolved from env fallbacks
        mock_projects_service.get_with_env_fallbacks.assert_called_once()
        assert experiment.project_id == mock_project.id

    @patch("galileo.experiment.Projects")
    def test_get_raises_error_when_no_project_and_no_env_fallback(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test get() raises ValueError when no project and no env fallback."""
        # Given: env fallback returns None (no project found)
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = None

        # When/Then: calling get() raises ResourceNotFoundError with helpful message
        with pytest.raises(ResourceNotFoundError, match="Project not found"):
            Experiment.get(name="Test Experiment")

    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_list_uses_env_fallback_when_no_project_specified(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test list() uses Projects().get_with_env_fallbacks() when no project is specified."""
        # Given: env fallback resolves to a project
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.list.return_value = []

        # When: calling list() without project params
        experiments = Experiment.list()

        # Then: project is resolved from env fallbacks
        mock_projects_service.get_with_env_fallbacks.assert_called_once()
        assert experiments == []

    @patch("galileo.experiment.Projects")
    def test_list_raises_error_when_no_project_and_no_env_fallback(
        self, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test list() raises ValueError when no project and no env fallback."""
        # Given: env fallback returns None (no project found)
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = None

        # When/Then: calling list() raises ResourceNotFoundError with helpful message
        with pytest.raises(ResourceNotFoundError, match="Project not found"):
            Experiment.list()


class TestExperimentCreate:
    """Test suite for Experiment.create() method."""

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_create_persists_and_triggers_experiment(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test create() persists the experiment with trigger=True and updates attributes."""
        # Given: mocks for project, dataset, prompt, metrics
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_prompt = MagicMock()
        mock_prompt.selected_version_id = str(uuid4())
        mock_get_prompt.return_value = mock_prompt

        mock_create_metrics.return_value = (None, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None
        mock_experiments_service.create.return_value = mock_experiment_response

        # When: create experiment
        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        ).create()

        # Then: create called with trigger=True
        mock_experiments_service.create.assert_called_once()
        call_kwargs = mock_experiments_service.create.call_args.kwargs
        assert call_kwargs["trigger"] is True
        assert call_kwargs["prompt_template"] == mock_prompt
        assert experiment.id == mock_experiment_response.id
        assert experiment.is_synced()
        assert experiment._run_result is not None

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_create_handles_existing_experiment_with_timestamp(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test create() adds timestamp when experiment with same name exists."""
        # Given: existing experiment with same name
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_get_prompt.return_value = MagicMock()
        mock_create_metrics.return_value = (None, [])

        existing_experiment = MagicMock()
        existing_experiment.name = "Test Experiment"

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = existing_experiment
        mock_experiments_service.create.return_value = mock_experiment_response

        # When: create experiment
        Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        ).create()

        # Then: name was changed (should have timestamp appended)
        call_args = mock_experiments_service.create.call_args
        assert "Test Experiment" in call_args.kwargs["name"]
        assert call_args.kwargs["name"] != "Test Experiment"

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_create_handles_api_failure(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_project: MagicMock,
    ) -> None:
        """Test create() handles API failures and sets state correctly."""
        # Given: API create fails
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_get_prompt.return_value = MagicMock()
        mock_create_metrics.return_value = (None, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None
        mock_experiments_service.create.side_effect = Exception("API Error")

        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_id="test-project-id"
        )

        # When/Then: create raises error and sets failed state
        with pytest.raises(Exception, match="API Error"):
            experiment.create()

        assert experiment.sync_state == SyncState.FAILED_SYNC

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_create_fills_default_prompt_settings_for_prompt_template(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test create() fills default PromptRunSettings when prompt template is present
        but no prompt_settings and no model_alias are provided."""
        # Given: prompt template resolved, no prompt_settings, no model_alias
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_prompt = MagicMock()
        mock_prompt.selected_version_id = str(uuid4())
        mock_get_prompt.return_value = mock_prompt

        mock_create_metrics.return_value = (None, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None
        mock_experiments_service.create.return_value = mock_experiment_response

        # When: create experiment with prompt but no settings
        Experiment(
            name="Test Experiment",
            dataset_name="test-dataset",
            prompt_name="test-prompt",
            project_name="Test Project",
            # No prompt_settings, no model
        ).create()

        # Then: default prompt settings are passed (not None)
        call_kwargs = mock_experiments_service.create.call_args.kwargs
        assert call_kwargs["prompt_settings"] is not None
        assert call_kwargs["prompt_settings"].model_alias == "GPT-4o"
        assert call_kwargs["prompt_settings"].temperature == 0.8
        assert call_kwargs["prompt_settings"].max_tokens == 256

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_create_preserves_user_prompt_settings_when_overriding_model_alias(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Regression for sc-61307: user-provided prompt_settings fields must not be dropped
        when model_alias is also supplied."""
        # Given: user supplies both prompt_settings (with non-default values) and model_alias
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_prompt = MagicMock()
        mock_prompt.selected_version_id = str(uuid4())
        mock_get_prompt.return_value = mock_prompt

        mock_create_metrics.return_value = (None, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None
        mock_experiments_service.create.return_value = mock_experiment_response

        user_settings = PromptRunSettings(temperature=0.42, max_tokens=123, top_p=0.9)

        # When: creating the experiment with both prompt_settings and model_alias
        Experiment(
            name="Test Experiment",
            dataset_name="test-dataset",
            prompt_name="test-prompt",
            project_name="Test Project",
            prompt_settings=user_settings,
            model="GPT-4o",
        ).create()

        # Then: user-provided fields survive and model_alias is applied on top
        call_kwargs = mock_experiments_service.create.call_args.kwargs
        effective = call_kwargs["prompt_settings"]
        assert effective.model_alias == "GPT-4o"
        assert effective.temperature == 0.42
        assert effective.max_tokens == 123
        assert effective.top_p == 0.9

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_create_treats_not_found_as_no_existing_experiment(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test create() succeeds when experiments_service.get() raises NotFoundError (no existing experiment)."""
        # Given: get() raises NotFoundError (experiment with that name doesn't exist yet)
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_prompt = MagicMock()
        mock_prompt.selected_version_id = str(uuid4())
        mock_get_prompt.return_value = mock_prompt

        mock_create_metrics.return_value = (None, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.side_effect = NotFoundError(404, b"Not Found")
        mock_experiments_service.create.return_value = mock_experiment_response

        # When: creating the experiment
        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        ).create()

        # Then: create() treats NotFoundError as "no existing experiment" and proceeds
        mock_experiments_service.create.assert_called_once()
        assert experiment.id == mock_experiment_response.id
        assert experiment.name == mock_experiment_response.name
        assert experiment.created_at == mock_experiment_response.created_at
        assert experiment.updated_at == mock_experiment_response.updated_at
        assert experiment.additional_properties == mock_experiment_response.additional_properties
        assert experiment.is_synced()


class TestExperimentGet:
    """Test suite for Experiment.get() class method."""

    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
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

    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
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

    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
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
    """Test suite for Experiment.run() method — now a no-op since create() triggers."""

    def test_run_returns_stored_result_from_create(self, reset_configuration: None) -> None:
        """Test run() returns the ExperimentRunResult stored during create()."""
        # Given: an experiment with _run_result set (as create() would do)
        experiment = Experiment._create_empty()
        experiment.name = "Test Experiment"
        experiment.id = str(uuid4())
        experiment.project_id = str(uuid4())
        experiment._experiment_response = MagicMock(spec=ExperimentResponse)
        experiment._run_result = ExperimentRunResult(
            {
                "experiment": experiment._experiment_response,
                "link": "http://test.com/results",
                "message": "Experiment started",
            }
        )

        # When: run() is called
        run_result = experiment.run()

        # Then: returns the stored result (no API call)
        assert isinstance(run_result, ExperimentRunResult)
        assert run_result.link == "http://test.com/results"

    @patch("galileo.experiment.ExperimentsService")
    def test_run_returns_fallback_result_when_no_stored_result(
        self, mock_experiments_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test run() returns a fallback result for experiments loaded via get()."""
        # Given: an experiment loaded via get() (no _run_result)
        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.config.console_url = "http://console.test.com"

        experiment = Experiment._create_empty()
        experiment.name = "Test Experiment"
        experiment.id = str(uuid4())
        experiment.project_id = str(uuid4())
        experiment._experiment_response = MagicMock(spec=ExperimentResponse)

        # When: run() is called without _run_result
        run_result = experiment.run()

        # Then: returns a fallback result with link
        assert isinstance(run_result, ExperimentRunResult)
        assert experiment.id in run_result.link

    def test_run_raises_error_when_not_created(self, reset_configuration: None) -> None:
        """Test run() raises error when experiment hasn't been created."""
        experiment = Experiment(
            name="Test", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        )

        with pytest.raises(ValueError, match="Experiment must be created before running"):
            experiment.run()

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_run_raises_error_on_second_call_after_result_consumed(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test run() raises ValueError when called a second time after the cached result has been consumed."""
        # Given: an experiment created via the normal create() flow
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_prompt = MagicMock()
        mock_prompt.selected_version_id = str(uuid4())
        mock_get_prompt.return_value = mock_prompt

        mock_create_metrics.return_value = (None, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None
        mock_experiments_service.create.return_value = mock_experiment_response
        mock_experiments_service.config.console_url = "http://console.test.com"

        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        ).create()

        # When: run() is called the first time — consumes the cached result
        first_result = experiment.run()
        assert isinstance(first_result, ExperimentRunResult)

        # Then: run() called a second time raises ValueError with "has already been run"
        with pytest.raises(ValueError, match="has already been run"):
            experiment.run()

    @patch("galileo.experiment.create_metric_configs")
    @patch("galileo.experiment.get_prompt")
    @patch("galileo.experiment.load_dataset_and_records")
    @patch("galileo.experiment.Projects")
    @patch("galileo.experiment.ExperimentsService")
    def test_create_run_create_run_resets_consumed_flag(
        self,
        mock_experiments_class: MagicMock,
        mock_projects_class: MagicMock,
        mock_load_dataset: MagicMock,
        mock_get_prompt: MagicMock,
        mock_create_metrics: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Regression for sc-61309: a second create() must reset _run_result_consumed
        so the following run() returns the new cached result instead of raising."""
        # Given: a fully mocked create() flow
        mock_projects_service = MagicMock()
        mock_projects_class.return_value = mock_projects_service
        mock_projects_service.get_with_env_fallbacks.return_value = mock_project

        mock_dataset = MagicMock()
        mock_load_dataset.return_value = (mock_dataset, [])

        mock_prompt = MagicMock()
        mock_prompt.selected_version_id = str(uuid4())
        mock_get_prompt.return_value = mock_prompt

        mock_create_metrics.return_value = (None, [])

        mock_experiments_service = MagicMock()
        mock_experiments_class.return_value = mock_experiments_service
        mock_experiments_service.get.return_value = None
        mock_experiments_service.create.return_value = mock_experiment_response
        mock_experiments_service.config.console_url = "http://console.test.com"

        # When: create() -> run() -> create() -> run()
        experiment = Experiment(
            name="Test Experiment", dataset_name="test-dataset", prompt_name="test-prompt", project_name="Test Project"
        ).create()
        first_run = experiment.run()
        assert experiment._run_result_consumed is True

        experiment.create()

        # Then: the second create() resets the consumed flag and re-populates _run_result
        assert experiment._run_result_consumed is False
        assert experiment._run_result is not None

        second_run = experiment.run()
        assert isinstance(first_run, ExperimentRunResult)
        assert isinstance(second_run, ExperimentRunResult)


class TestExperimentQuery:
    """Test suite for Experiment query methods."""

    @patch("galileo.experiment.Search")
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

    @patch("galileo.project.Project")
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

    @patch("galileo.experiment.GalileoPythonConfig")
    @patch("galileo.experiment.get_experiment_projects_project_id_experiments_experiment_id_get")
    def test_refresh_updates_attributes(
        self,
        mock_get_experiment_api: MagicMock,
        mock_config_class: MagicMock,
        synced_experiment: Experiment,
        mock_experiment_response: MagicMock,
        reset_configuration: None,
    ) -> None:
        """Test refresh() updates all synced attributes from API."""
        # Given: a synced experiment with a stale name and mocked GET-by-ID API response
        mock_config = MagicMock()
        mock_config_class.get.return_value = mock_config
        mock_get_experiment_api.sync.return_value = mock_experiment_response

        synced_experiment.name = "Old Name"
        original_project_id = synced_experiment.project_id
        original_experiment_id = synced_experiment.id

        # When: refresh() is called
        synced_experiment.refresh()

        # Then: GET-by-ID called with correct project_id and experiment_id
        mock_get_experiment_api.sync.assert_called_once_with(
            project_id=original_project_id, experiment_id=original_experiment_id, client=mock_config.api_client
        )
        # Then: all top-level attributes are updated from API response
        assert synced_experiment.id == mock_experiment_response.id
        assert synced_experiment.name == mock_experiment_response.name
        assert synced_experiment.created_at == mock_experiment_response.created_at
        assert synced_experiment.updated_at == mock_experiment_response.updated_at
        assert synced_experiment.additional_properties == mock_experiment_response.additional_properties
        # dataset is None in the response — fields cleared
        assert synced_experiment.dataset_id is None
        assert synced_experiment.dataset_name is None
        # prompt is None in the response — locally-set values are preserved
        assert synced_experiment.prompt_id is None
        assert synced_experiment.prompt_name is None
        # prompt_run_settings is None — prompt_settings and model_alias cleared
        assert synced_experiment.prompt_settings is None
        assert synced_experiment.model_alias is None
        # cached API response is updated
        assert synced_experiment._experiment_response is mock_experiment_response
        assert synced_experiment.is_synced()

    @patch("galileo.experiment.GalileoPythonConfig")
    @patch("galileo.experiment.get_experiment_projects_project_id_experiments_experiment_id_get")
    def test_refresh_sets_failed_sync_on_not_found(
        self,
        mock_get_experiment_api: MagicMock,
        mock_config_class: MagicMock,
        synced_experiment: Experiment,
        reset_configuration: None,
    ) -> None:
        """Test refresh() transitions to FAILED_SYNC when the GET-by-ID endpoint raises NotFoundError."""
        # Given: a synced experiment and the API raises NotFoundError (404)
        mock_config = MagicMock()
        mock_config_class.get.return_value = mock_config
        mock_get_experiment_api.sync.side_effect = NotFoundError(404, b"Not Found")

        # When/Then: refresh() raises NotFoundError and sets FAILED_SYNC
        with pytest.raises(NotFoundError):
            synced_experiment.refresh()

        assert synced_experiment.sync_state == SyncState.FAILED_SYNC

    @patch("galileo.experiment.GalileoPythonConfig")
    @patch("galileo.experiment.delete_experiment_projects_project_id_experiments_experiment_id_delete")
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
    @patch("galileo.experiment.Search")
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

    @patch("galileo.experiment.get_prompt")
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
    @patch("galileo.experiment.Search")
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

    @patch("galileo.experiment.GalileoPythonConfig")
    @patch("galileo.experiment.get_experiment_projects_project_id_experiments_experiment_id_get")
    def test_get_status_returns_status_info(
        self,
        mock_get_experiment_api: MagicMock,
        mock_config_class: MagicMock,
        synced_experiment: Experiment,
        mock_experiment_response: MagicMock,
        reset_configuration: None,
    ) -> None:
        """Test get_status() returns ExperimentStatusInfo."""
        # Given: a synced experiment and mocked GET-by-ID response
        mock_config = MagicMock()
        mock_config_class.get.return_value = mock_config
        mock_get_experiment_api.sync.return_value = mock_experiment_response

        synced_experiment._experiment_response = mock_experiment_response

        # When: get_status() is called (internally calls refresh())
        status = synced_experiment.get_status()

        # Then: returns ExperimentStatusInfo
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

    @patch("galileo.experiment.GalileoPythonConfig")
    @patch("galileo.experiment.get_experiment_projects_project_id_experiments_experiment_id_get")
    @patch("galileo.experiment.upsert_experiment_tag")
    def test_add_tag_upserts_tag(
        self,
        mock_upsert_tag: MagicMock,
        mock_get_experiment_api: MagicMock,
        mock_config_class: MagicMock,
        reset_configuration: None,
        mock_experiment_response: MagicMock,
    ) -> None:
        """Test add_tag() upserts tag via API."""
        # Given: a synced experiment with known IDs and mocked refresh API
        exp_id = str(uuid4())
        proj_id = str(uuid4())

        mock_experiment_response.id = exp_id
        mock_experiment_response.name = "Test"

        mock_config = MagicMock()
        mock_config_class.get.return_value = mock_config
        mock_get_experiment_api.sync.return_value = mock_experiment_response

        experiment = Experiment._create_empty()
        experiment.id = exp_id
        experiment.project_id = proj_id
        experiment.name = "Test"
        experiment._set_state(SyncState.SYNCED)

        # When: adding a tag
        experiment.add_tag("environment", "production")

        # Then: the tag is upserted via API
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
    @patch("galileo.experiment.GalileoPythonConfig")
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
        with patch(f"galileo.experiment.{api_function}") as mock_api:
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
