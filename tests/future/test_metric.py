from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import LlmMetric, Metric
from galileo.__future__.shared.base import SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.resources.models import OutputTypeEnum, ScorerTypes
from galileo_core.schemas.logging.step import StepType


class TestMetricInitialization:
    """Test suite for Metric initialization."""

    def test_init_with_required_fields(self, reset_configuration: None) -> None:
        """Test initializing a metric with required fields creates a local-only instance."""
        metric = LlmMetric(
            name="Test Metric", prompt="Is the response factually accurate?", model="gpt-4.1-mini", judges=3
        )

        assert metric.name == "Test Metric"
        assert metric.prompt == "Is the response factually accurate?"
        assert metric.model == "gpt-4.1-mini"
        assert metric.judges == 3
        assert metric.scorer_type == ScorerTypes.LLM
        assert metric.id is None
        assert metric.sync_state == SyncState.LOCAL_ONLY

    def test_init_with_all_fields(self, reset_configuration: None) -> None:
        """Test initializing a metric with all fields."""
        metric = LlmMetric(
            name="Test Metric",
            prompt="Is the response factually accurate?",
            node_level=StepType.llm,
            cot_enabled=True,
            model="gpt-4.1-mini",
            judges=5,
            description="Test metric description",
            tags=["test", "factuality"],
            output_type="percentage",
        )

        assert metric.name == "Test Metric"
        assert metric.prompt == "Is the response factually accurate?"
        assert metric.scorer_type == ScorerTypes.LLM
        assert metric.node_level == StepType.llm
        assert metric.cot_enabled is True
        assert metric.model == "gpt-4.1-mini"
        assert metric.judges == 5
        assert metric.description == "Test metric description"
        assert metric.tags == ["test", "factuality"]
        assert metric.output_type == OutputTypeEnum.PERCENTAGE

    def test_init_without_name_raises_error(self, reset_configuration: None) -> None:
        """Test initializing a metric without name raises TypeError."""
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            # name is a required positional argument - omit it entirely
            LlmMetric(prompt="Test prompt")  # type: ignore[call-arg]

    def test_init_llm_scorer_without_user_prompt_raises_error(self, reset_configuration: None) -> None:
        """Test initializing an LLM metric without prompt raises ValidationError."""
        with pytest.raises(ValidationError, match="'prompt' .* must be provided for LLM-based metrics"):
            LlmMetric(name="Test Metric", prompt=None)


class TestMetricCreate:
    """Test suite for Metric.create() method."""

    @patch("galileo.__future__.metric.Metrics")
    @patch("galileo.__future__.metric.Scorers")
    def test_create_persists_metric_to_api(
        self, mock_scorers_class: MagicMock, mock_metrics_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test create() persists the metric to the API and updates attributes."""
        mock_metrics_service = MagicMock()
        mock_metrics_class.return_value = mock_metrics_service

        mock_scorers_service = MagicMock()
        mock_scorers_class.return_value = mock_scorers_service

        scorer_id = str(uuid4())
        mock_version = MagicMock()
        mock_version.scorer_id = scorer_id
        mock_version.created_at = MagicMock()
        mock_version.updated_at = MagicMock()

        mock_scorer = MagicMock()
        mock_scorer.id = scorer_id
        mock_scorer.name = "Test Metric"
        mock_scorer.scorer_type = ScorerTypes.LLM
        mock_scorer.tags = ["test"]
        mock_scorer.description = "Test description"
        mock_scorer.created_at = MagicMock()
        mock_scorer.updated_at = MagicMock()
        mock_scorer.output_type = OutputTypeEnum.BOOLEAN
        mock_scorer.user_prompt = "Is it accurate?"
        mock_scorer.defaults = MagicMock()
        mock_scorer.defaults.model_name = "gpt-4.1-mini"
        mock_scorer.defaults.num_judges = 3
        mock_scorer.defaults.cot_enabled = True
        mock_scorer.scoreable_node_types = ["llm"]

        mock_metrics_service.create_custom_llm_metric.return_value = mock_version
        mock_scorers_service.list.return_value = [mock_scorer]

        metric = LlmMetric(
            name="Test Metric", user_prompt="Is it accurate?", description="Test description", tags=["test"]
        ).create()

        mock_metrics_service.create_custom_llm_metric.assert_called_once()
        assert metric.id == scorer_id
        assert metric.is_synced()

    @patch("galileo.__future__.metric.Metrics")
    def test_create_handles_api_failure(self, mock_metrics_class: MagicMock, reset_configuration: None) -> None:
        """Test create() handles API failures and sets state correctly."""
        mock_service = MagicMock()
        mock_metrics_class.return_value = mock_service
        mock_service.create_custom_llm_metric.side_effect = Exception("API Error")

        metric = LlmMetric(name="Test Metric", prompt="Is it accurate?")

        with pytest.raises(Exception, match="API Error"):
            metric.create()

        assert metric.sync_state == SyncState.FAILED_SYNC

    @patch("galileo.__future__.metric.Metrics")
    def test_create_non_llm_scorer_raises_not_implemented(
        self, mock_metrics_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test create() with non-LLM scorer type raises NotImplementedError."""
        # Test that CodeMetric.create() raises NotImplementedError
        from galileo.__future__ import CodeMetric

        metric = CodeMetric(name="Test Metric")

        with pytest.raises(NotImplementedError, match="not yet supported"):
            metric.create()


class TestMetricGet:
    """Test suite for Metric.get() class method."""

    @patch("galileo.__future__.metric.Scorers")
    def test_get_by_name_returns_metric(self, mock_scorers_class: MagicMock, reset_configuration: None) -> None:
        """Test get() with name returns a synced metric instance."""
        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service

        mock_scorer = MagicMock()
        mock_scorer.id = str(uuid4())
        mock_scorer.name = "Test Metric"
        mock_scorer.scorer_type = ScorerTypes.LLM
        mock_scorer.tags = []
        mock_scorer.description = "Test"
        mock_scorer.created_at = MagicMock()
        mock_scorer.updated_at = MagicMock()
        mock_scorer.output_type = OutputTypeEnum.BOOLEAN
        mock_scorer.user_prompt = "Test"
        mock_scorer.defaults = MagicMock()
        mock_scorer.defaults.model_name = "gpt-4.1-mini"
        mock_scorer.defaults.num_judges = 3
        mock_scorer.defaults.cot_enabled = True
        mock_scorer.scoreable_node_types = ["llm"]

        mock_service.list.return_value = [mock_scorer]

        metric = Metric.get(name="Test Metric")

        assert metric is not None
        assert metric.name == "Test Metric"
        assert metric.is_synced()

    @patch("galileo.__future__.metric.Scorers")
    def test_get_by_id_returns_metric(self, mock_scorers_class: MagicMock, reset_configuration: None) -> None:
        """Test get() with id returns a synced metric instance."""
        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service

        metric_id = str(uuid4())
        mock_scorer = MagicMock()
        mock_scorer.id = metric_id
        mock_scorer.name = "Test Metric"
        mock_scorer.scorer_type = ScorerTypes.LLM
        mock_scorer.tags = []
        mock_scorer.description = "Test"
        mock_scorer.created_at = MagicMock()
        mock_scorer.updated_at = MagicMock()
        mock_scorer.output_type = OutputTypeEnum.BOOLEAN
        mock_scorer.user_prompt = "Test"
        mock_scorer.defaults = MagicMock()
        mock_scorer.scoreable_node_types = []

        mock_service.list.return_value = [mock_scorer]

        metric = Metric.get(id=metric_id)

        assert metric is not None
        assert metric.id == metric_id
        assert metric.is_synced()

    @patch("galileo.__future__.metric.Scorers")
    def test_get_returns_none_when_not_found(self, mock_scorers_class: MagicMock, reset_configuration: None) -> None:
        """Test get() returns None when metric is not found."""
        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service
        mock_service.list.return_value = []

        metric = Metric.get(name="Nonexistent Metric")

        assert metric is None

    @pytest.mark.parametrize(
        "kwargs,expected_error",
        [
            ({"id": "test-id", "name": "Test"}, "Cannot specify both id and name"),
            ({}, "Must specify either id or name"),
        ],
    )
    def test_get_validates_parameters(self, kwargs: dict, expected_error: str, reset_configuration: None) -> None:
        """Test get() validates parameter combinations."""
        with pytest.raises(ValidationError, match=expected_error):
            Metric.get(**kwargs)


class TestMetricList:
    """Test suite for Metric.list() class method."""

    @patch("galileo.__future__.metric.Scorers")
    def test_list_returns_all_metrics(self, mock_scorers_class: MagicMock, reset_configuration: None) -> None:
        """Test list() returns a list of synced metric instances."""
        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service

        # Create 3 mock metrics
        mock_scorers = []
        for i in range(3):
            mock_scorer = MagicMock()
            mock_scorer.id = str(uuid4())
            mock_scorer.name = f"Metric {i}"
            mock_scorer.scorer_type = ScorerTypes.LLM
            mock_scorer.tags = []
            mock_scorer.description = f"Description {i}"
            mock_scorer.created_at = MagicMock()
            mock_scorer.updated_at = MagicMock()
            mock_scorer.output_type = OutputTypeEnum.BOOLEAN
            mock_scorer.user_prompt = f"Prompt {i}"
            mock_scorer.defaults = MagicMock()
            mock_scorer.scoreable_node_types = []
            mock_scorers.append(mock_scorer)

        mock_service.list.return_value = mock_scorers

        metrics = Metric.list()

        assert len(metrics) == 3
        assert all(isinstance(m, Metric) for m in metrics)
        assert all(m.is_synced() for m in metrics)

    @patch("galileo.__future__.metric.Scorers")
    def test_list_with_name_filter(self, mock_scorers_class: MagicMock, reset_configuration: None) -> None:
        """Test list() with name filter."""
        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service

        mock_scorer = MagicMock()
        mock_scorer.id = str(uuid4())
        mock_scorer.name = "Factuality Metric"
        mock_scorer.scorer_type = ScorerTypes.LLM
        mock_scorer.tags = []
        mock_scorer.description = "Test"
        mock_scorer.created_at = MagicMock()
        mock_scorer.updated_at = MagicMock()
        mock_scorer.output_type = OutputTypeEnum.BOOLEAN
        mock_scorer.user_prompt = "Test"
        mock_scorer.defaults = MagicMock()
        mock_scorer.scoreable_node_types = []

        mock_service.list.return_value = [mock_scorer]

        metrics = Metric.list(name_filter="Factuality Metric")

        mock_service.list.assert_called_once_with(name="Factuality Metric", types=None)
        assert len(metrics) == 1
        assert metrics[0].name == "Factuality Metric"

    @patch("galileo.__future__.metric.Scorers")
    def test_list_with_scorer_types_filter(self, mock_scorers_class: MagicMock, reset_configuration: None) -> None:
        """Test list() with scorer types filter."""
        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service
        mock_service.list.return_value = []

        Metric.list(scorer_types=[ScorerTypes.LLM])

        mock_service.list.assert_called_once_with(name=None, types=[ScorerTypes.LLM])


class TestMetricDelete:
    """Test suite for Metric.delete() method."""

    @patch("galileo.__future__.metric.Metrics")
    @patch("galileo.__future__.metric.Scorers")
    def test_delete_removes_metric(
        self, mock_scorers_class: MagicMock, mock_metrics_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test delete() removes the metric."""
        mock_scorers_service = MagicMock()
        mock_scorers_class.return_value = mock_scorers_service

        mock_metrics_service = MagicMock()
        mock_metrics_class.return_value = mock_metrics_service

        metric_id = str(uuid4())
        mock_scorer = MagicMock()
        mock_scorer.id = metric_id
        mock_scorer.name = "Test Metric"
        mock_scorer.scorer_type = ScorerTypes.LLM
        mock_scorer.tags = []
        mock_scorer.description = "Test"
        mock_scorer.created_at = MagicMock()
        mock_scorer.updated_at = MagicMock()
        mock_scorer.output_type = OutputTypeEnum.BOOLEAN
        mock_scorer.user_prompt = "Test"
        mock_scorer.defaults = MagicMock()
        mock_scorer.scoreable_node_types = []

        mock_scorers_service.list.return_value = [mock_scorer]

        metric = Metric.get(id=metric_id)
        metric.delete()

        mock_metrics_service.delete_metric.assert_called_once_with(name="Test Metric")
        assert metric.sync_state == SyncState.DELETED

    def test_delete_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test delete() raises ValueError for local-only metric."""
        metric = LlmMetric(name="Test Metric", prompt="Test prompt")

        with pytest.raises(ValueError, match="Metric ID is not set"):
            metric.delete()


class TestMetricRefresh:
    """Test suite for Metric.refresh() method."""

    @patch("galileo.__future__.metric.Scorers")
    def test_refresh_updates_attributes(self, mock_scorers_class: MagicMock, reset_configuration: None) -> None:
        """Test refresh() updates all attributes from the API."""
        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service

        metric_id = str(uuid4())

        # Initial state
        initial_scorer = MagicMock()
        initial_scorer.id = metric_id
        initial_scorer.name = "Test Metric"
        initial_scorer.scorer_type = ScorerTypes.LLM
        initial_scorer.tags = ["test"]
        initial_scorer.description = "Initial description"
        initial_scorer.created_at = MagicMock()
        initial_scorer.updated_at = MagicMock()
        initial_scorer.output_type = OutputTypeEnum.BOOLEAN
        initial_scorer.user_prompt = "Initial prompt"
        initial_scorer.defaults = MagicMock()
        initial_scorer.defaults.model_name = "gpt-4.1-mini"
        initial_scorer.defaults.num_judges = 3
        initial_scorer.defaults.cot_enabled = True
        initial_scorer.scoreable_node_types = ["llm"]

        # Updated state
        updated_scorer = MagicMock()
        updated_scorer.id = metric_id
        updated_scorer.name = "Test Metric"
        updated_scorer.scorer_type = ScorerTypes.LLM
        updated_scorer.tags = ["test", "updated"]
        updated_scorer.description = "Updated description"
        updated_scorer.created_at = initial_scorer.created_at
        updated_scorer.updated_at = MagicMock()
        updated_scorer.output_type = OutputTypeEnum.BOOLEAN
        updated_scorer.user_prompt = "Updated prompt"
        updated_scorer.defaults = MagicMock()
        updated_scorer.defaults.model_name = "gpt-4o"
        updated_scorer.defaults.num_judges = 5
        updated_scorer.defaults.cot_enabled = False
        updated_scorer.scoreable_node_types = ["llm"]

        mock_service.list.side_effect = [[initial_scorer], [updated_scorer]]

        metric = Metric.get(id=metric_id)
        assert metric.description == "Initial description"
        assert metric.judges == 3

        metric.refresh()

        assert metric.description == "Updated description"
        assert metric.judges == 5
        assert metric.is_synced()

    def test_refresh_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test refresh() raises ValueError for local-only metric."""
        metric = LlmMetric(name="Test Metric", prompt="Test prompt")

        with pytest.raises(ValueError, match="Metric ID is not set"):
            metric.refresh()

    @patch("galileo.__future__.metric.Scorers")
    def test_refresh_raises_error_when_metric_no_longer_exists(
        self, mock_scorers_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test refresh() raises error when metric no longer exists."""
        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service

        metric_id = str(uuid4())
        mock_scorer = MagicMock()
        mock_scorer.id = metric_id
        mock_scorer.name = "Test Metric"
        mock_scorer.scorer_type = ScorerTypes.LLM
        mock_scorer.tags = []
        mock_scorer.description = "Test"
        mock_scorer.created_at = MagicMock()
        mock_scorer.updated_at = MagicMock()
        mock_scorer.output_type = OutputTypeEnum.BOOLEAN
        mock_scorer.user_prompt = "Test"
        mock_scorer.defaults = MagicMock()
        mock_scorer.scoreable_node_types = []

        # First call returns the metric, second returns empty list (deleted)
        mock_service.list.side_effect = [[mock_scorer], []]

        metric = Metric.get(id=metric_id)

        with pytest.raises(ValueError, match="no longer exists"):
            metric.refresh()


class TestMetricUpdate:
    """Test suite for Metric.update() method."""

    def test_update_raises_not_implemented_error(self, reset_configuration: None) -> None:
        """Test update() raises NotImplementedError."""
        metric = LlmMetric(name="Test Metric", prompt="Test prompt")

        with pytest.raises(NotImplementedError, match="not yet supported"):
            metric.update(name="New Name")


class TestMetricMethods:
    """Test suite for other Metric methods."""

    def test_str_and_repr(self, reset_configuration: None) -> None:
        """Test __str__ and __repr__ return expected formats."""
        metric = LlmMetric(name="Test Metric", prompt="Is it accurate?", output_type="percentage")
        metric.id = "test-id-123"

        assert str(metric) == "LlmMetric(name='Test Metric', id='test-id-123', scorer_type='llm')"
        assert "model=" in repr(metric) and "judges=" in repr(metric)

    @patch("galileo.__future__.metric.Scorers")
    def test_populate_from_scorer_response_handles_unset_values(
        self, mock_scorers_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test _populate_from_scorer_response handles Unset values correctly."""
        from galileo.resources.types import Unset as UnsetType

        mock_service = MagicMock()
        mock_scorers_class.return_value = mock_service

        mock_scorer = MagicMock()
        mock_scorer.id = str(uuid4())
        mock_scorer.name = "Test Metric"
        mock_scorer.scorer_type = ScorerTypes.LLM
        mock_scorer.tags = []
        mock_scorer.description = UnsetType()
        mock_scorer.created_at = UnsetType()
        mock_scorer.updated_at = UnsetType()
        mock_scorer.output_type = UnsetType()
        mock_scorer.user_prompt = UnsetType()
        mock_scorer.defaults = UnsetType()
        mock_scorer.scoreable_node_types = UnsetType()

        mock_service.list.return_value = [mock_scorer]

        metric = Metric.get(name="Test Metric")

        assert metric is not None
        assert metric.description == ""
        assert metric.created_at is None
        assert metric.updated_at is None
        assert metric.output_type is None
        assert metric.prompt is None
        assert metric.model is None
        assert metric.judges is None
        assert metric.cot_enabled is None
        assert metric.node_level is None
