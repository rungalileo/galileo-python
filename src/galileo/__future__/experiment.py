from __future__ import annotations

import builtins
import datetime
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.__future__.shared.experiment_result import ExperimentRunResult, ExperimentStatusInfo
from galileo.__future__.shared.query_result import QueryResult
from galileo.config import GalileoPythonConfig
from galileo.datasets import Dataset as LegacyDataset
from galileo.experiment_tags import upsert_experiment_tag
from galileo.experiments import Experiments as ExperimentsService
from galileo.export import ExportClient
from galileo.job_progress import get_run_scorer_jobs, job_progress
from galileo.projects import Projects
from galileo.prompts import PromptTemplate, get_prompt
from galileo.resources.api.experiment import delete_experiment_projects_project_id_experiments_experiment_id_delete
from galileo.resources.api.trace import (
    sessions_available_columns_projects_project_id_sessions_available_columns_post,
    spans_available_columns_projects_project_id_spans_available_columns_post,
    traces_available_columns_projects_project_id_traces_available_columns_post,
)
from galileo.resources.models import (
    ExperimentResponse,
    HTTPValidationError,
    LLMExportFormat,
    LogRecordsSortClause,
    PromptRunSettings,
    RootType,
    ScorerConfig,
)
from galileo.resources.models.log_records_available_columns_request import LogRecordsAvailableColumnsRequest
from galileo.resources.models.log_records_available_columns_response import LogRecordsAvailableColumnsResponse
from galileo.resources.types import Unset

# TODO: DatasetRecord needed for function-based experiments
# from galileo.schema.datasets import DatasetRecord
from galileo.schema.filters import FilterType
from galileo.schema.metrics import GalileoMetrics, LocalMetricConfig, Metric
from galileo.search import RecordType, Search

# TODO: get_records_for_dataset needed for function-based experiments
# from galileo.utils.datasets import get_records_for_dataset, load_dataset_and_records
from galileo.utils.datasets import load_dataset_and_records
from galileo.utils.logging import get_logger
from galileo.utils.metrics import create_metric_configs
from galileo.utils.validations import require_exactly_one

if TYPE_CHECKING:
    from galileo.__future__.dataset import Dataset
    from galileo.__future__.project import Project
    from galileo.__future__.prompt import Prompt
    from galileo.__future__.shared.column import ColumnCollection

_logger = get_logger(__name__)

EXPERIMENT_TASK_TYPE: int = 16

# Mapping from RecordType (plural) to RootType (singular)
RECORD_TYPE_TO_ROOT_TYPE = {
    RecordType.SPAN: RootType.SPAN,
    RecordType.TRACE: RootType.TRACE,
    RecordType.SESSION: RootType.SESSION,
}


class Experiment(StateManagementMixin):
    """
    Object-centric interface for Galileo experiments.

    An experiment represents a systematic evaluation framework for running controlled
    tests on datasets to measure and compare AI model performance.

    Important Notes
    ---------------
    **Two-Phase Execution:**
        Experiments are created in two phases:
        1. Create the experiment metadata (name, dataset, optional prompt)
        2. Run the experiment by creating a job that executes on the dataset

        This allows you to set up the experiment structure before execution.

    **Prompt Settings Hierarchy:**
        When running an experiment with a prompt template, the prompt_settings parameter
        passed to run() completely overrides any settings stored in the prompt template
        itself. The Runners service uses ONLY the settings provided at job creation time.

        If you don't provide prompt_settings to run(), default values will be used.
        To use the template's settings, retrieve them first using get_prompt_template_settings()
        and pass them explicitly.

    **Experiment Immutability:**
        Once an experiment has been run and has traces, it cannot be run again.
        To re-run with the same configuration, create a new experiment with a
        different name. This ensures experiment results remain comparable and auditable.

    **Dataset Requirements:**
        While dataset is optional during creation, it is required when running
        the experiment with either a prompt template or a function.

    Attributes
    ----------
        id (str | None): Unique experiment identifier.
        name (str): Experiment name.
        project_id (str | None): ID of parent project.
        project_name (str | None): Name of parent project (may be None if retrieved by project_id only).
        dataset_id (str | None): ID of associated dataset.
        dataset_name (str | None): Name of associated dataset.
        prompt_id (str | None): ID of associated prompt template.
        prompt_name (str | None): Name of associated prompt template.
        created_at (datetime | None): When experiment was created.
        updated_at (datetime | None): When experiment was last updated.
        metrics (list | None): List of metrics to evaluate.
        prompt_settings (PromptRunSettings | None): Settings for prompt runs.
        additional_properties (dict): Additional experiment properties.

    Examples
    --------
        # Create an experiment
        experiment = Experiment(
            name="ml-expert-evaluation",
            dataset_name="ml-knowledge-dataset",
            prompt_name="ml-expert-v1",
            metrics=["correctness", "completeness"],
            project_name="My AI Project"
        )

        # Create and run
        experiment.create()
        result = experiment.run()

        # Check results
        experiment.refresh()
        metrics = experiment.aggregate_metrics
        print(f"Average cost: ${metrics['average_cost']}")

        # Re-run with different name
        experiment2 = Experiment(
            name=f"{experiment.name}-rerun-1",
            dataset_name=experiment.dataset_name,
            prompt_name=experiment.prompt_name,
            metrics=experiment.metrics,
            project_name=experiment.project_name
        ).create()
        experiment2.run()
    """

    id: str | None
    name: str
    project_id: str | None
    project_name: str | None
    dataset_id: str | None
    dataset_name: str | None
    prompt_id: str | None
    prompt_name: str | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    metrics: builtins.list[GalileoMetrics | Metric | LocalMetricConfig | str] | None
    # TODO: Function-based experiments temporarily disabled - need to validate implementation
    # function: Callable | None
    model_alias: str | None
    prompt_settings: PromptRunSettings | None
    additional_properties: dict[str, Any]

    # Private attributes for runtime state
    _dataset_obj: LegacyDataset | None
    _prompt_template: PromptTemplate | None
    _model_obj: Model | None
    _experiment_response: ExperimentResponse | None
    _job_id: str | None

    def __str__(self) -> str:
        """String representation of the experiment."""
        return f"Experiment(name='{self.name}', id='{self.id}', project_id='{self.project_id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the experiment."""
        return (
            f"Experiment(name='{self.name}', id='{self.id}', project_id='{self.project_id}', "
            f"created_at='{self.created_at}')"
        )

    @require_exactly_one("project_id", "project_name")
    @require_exactly_one("prompt", "prompt_name")  # TODO: For function-based experiments, prompt is optional.
    def __init__(
        self,
        name: str,
        *,
        dataset: Dataset | LegacyDataset | str | None = None,
        dataset_name: str | None = None,
        prompt: Prompt | PromptTemplate | str | None = None,
        prompt_name: str | None = None,
        model: Model | str | None = None,
        metrics: builtins.list[GalileoMetrics | Metric | LocalMetricConfig | str] | None = None,
        project_id: str | None = None,
        project_name: str | None = None,
        # TODO: Function-based experiments are temporarily disabled. Need to validate implementation and fix decorator logic.
        # function: Callable | None = None,
        prompt_settings: PromptRunSettings | None = None,
    ) -> None:
        """
        Initialize an Experiment instance locally.

        Creates a local experiment object that exists only in memory until .create()
        is called to persist it to the API.

        Args:
            name (str): The name of the experiment.
            dataset: Dataset object, dataset name, or legacy Dataset object. Optional at creation,
                    but required when running the experiment with a prompt template.
            dataset_name: Name of the dataset (alternative to dataset parameter). Optional at creation,
                         but required when running the experiment with a prompt template.
            prompt: Prompt object, prompt name, or legacy PromptTemplate object.
            prompt_name: Name of the prompt template (alternative to prompt parameter).
            model: Model object or model alias string to use for the experiment.
                  This will be used to configure the prompt_settings when running the experiment.
            metrics: List of metrics to evaluate.
            project_id: The project ID. Exactly one of project_id or project_name must be provided.
            project_name: The project name. Exactly one of project_id or project_name must be provided.
            prompt_settings: Settings for prompt runs. If provided along with model parameter,
                           the model parameter takes precedence.

        Raises
        ------
            ValidationError: If name is not provided, or if neither/both project_id and project_name are provided.

        Examples
        --------
            # Create by project name with dataset and prompt names
            experiment = Experiment(
                name="ml-evaluation",
                dataset_name="ml-dataset",
                prompt_name="ml-prompt",
                project_name="My AI Project"
            )

            # Create with object references and model
            experiment = Experiment(
                name="ml-evaluation",
                dataset=Dataset.get(name="ml-dataset"),
                prompt=Prompt.get(name="ml-prompt"),
                model="gpt-4o-mini",
                project_name="My AI Project"
            )
        """
        super().__init__()

        if not name:
            raise ValidationError("'name' must be provided to create an experiment.")

        # Initialize core attributes
        self.name = name
        self.project_id = project_id
        self.project_name = project_name
        self.id = None
        self.created_at = None
        self.updated_at = None
        self.additional_properties = {}

        # Initialize experiment-specific attributes
        self.metrics = metrics
        # TODO: Function-based experiments temporarily disabled - need to validate implementation
        # self.function = function
        self.prompt_settings = prompt_settings

        # Handle model parameter
        self.model_alias = None
        self._model_obj = None

        if model is not None:
            # Local import to avoid circular dependency
            from galileo.__future__.model import Model

            if isinstance(model, Model):
                self._model_obj = model
                self.model_alias = model.alias
            elif isinstance(model, str):
                self.model_alias = model

        # Handle dataset parameter
        self.dataset_id = None
        self.dataset_name = None
        self._dataset_obj = None

        # TODO: Improve serialization and delegate the responsibilities to the serializer.
        if dataset is not None:
            # Local import to avoid circular dependency
            from galileo.__future__.dataset import Dataset

            if isinstance(dataset, Dataset):
                self.dataset_id = dataset.id
                self.dataset_name = dataset.name
            elif isinstance(dataset, LegacyDataset):
                self._dataset_obj = dataset
                self.dataset_id = dataset.dataset.id if dataset.dataset else None
                self.dataset_name = dataset.dataset.name if dataset.dataset else None
            elif isinstance(dataset, str):
                self.dataset_name = dataset
        elif dataset_name is not None:
            self.dataset_name = dataset_name

        # Handle prompt parameter
        self.prompt_id = None
        self.prompt_name = None
        self._prompt_template = None

        # TODO: Delegate the responsibilities to the serializer.
        if prompt is not None:
            # Local import to avoid circular dependency
            from galileo.__future__.prompt import Prompt

            if isinstance(prompt, Prompt):
                self.prompt_id = prompt.id
                self.prompt_name = prompt.name
                _logger.debug(
                    f"Experiment.__init__: Prompt object provided - "
                    f"prompt_id='{self.prompt_id}', prompt_name='{self.prompt_name}'"
                )
            elif isinstance(prompt, PromptTemplate):
                self._prompt_template = prompt
                self.prompt_id = prompt.selected_version_id
                self.prompt_name = prompt.name
            elif isinstance(prompt, str):
                self.prompt_name = prompt
        elif prompt_name is not None:
            self.prompt_name = prompt_name

        # Private runtime state
        self._experiment_response = None
        self._job_id = None

        # Set initial state
        self._set_state(SyncState.LOCAL_ONLY)

    def create(self) -> Experiment:
        """
        Persist this experiment to the API.

        Returns
        -------
            Experiment: This experiment instance with updated attributes from the API.

        Raises
        ------
            ValueError: If the experiment name or project information is not set.
            Exception: If the API call fails.

        Examples
        --------
            experiment = Experiment(
                name="ml-evaluation",
                dataset_name="ml-dataset",
                project_name="My AI Project"
            ).create()
            assert experiment.is_synced()
        """
        if not self.name:
            raise ValueError("Experiment name is not set. Cannot create experiment without a name.")

        if not self.project_id and not self.project_name:
            raise ValueError(
                "Project information is not set. Cannot create experiment without project_id or project_name."
            )

        try:
            _logger.info(f"Experiment.create: name='{self.name}' project_id='{self.project_id}' - started")

            # Resolve project (prefer ID over name since get_with_env_fallbacks requires exactly one)
            project_obj = Projects().get_with_env_fallbacks(
                id=self.project_id if self.project_id else None, name=self.project_name if not self.project_id else None
            )
            if not project_obj:
                raise ValueError(f"Project not found: id={self.project_id}, name={self.project_name}")

            self.project_id = project_obj.id
            if self.project_name is None:
                self.project_name = project_obj.name

            # Load dataset if needed
            if self._dataset_obj is None and (self.dataset_id or self.dataset_name):
                self._dataset_obj, _ = load_dataset_and_records(
                    dataset=self.dataset_name or self.dataset_id,
                    dataset_id=self.dataset_id,
                    dataset_name=self.dataset_name,
                )

            # Check for existing experiment with same name
            experiments_service = ExperimentsService()
            existing_experiment = experiments_service.get(self.project_id, self.name)

            if existing_experiment:
                _logger.warning(f"Experiment {existing_experiment.name} already exists, adding a timestamp")
                now = datetime.datetime.now(datetime.timezone.utc)
                self.name = f"{existing_experiment.name} {now:%Y-%m-%d} at {now:%H:%M:%S}.{now.microsecond // 1000:03d}"

            # Create experiment
            created_experiment = experiments_service.create(
                project_id=self.project_id, name=self.name, dataset_obj=self._dataset_obj
            )

            # Update attributes from response
            # Note: prompt_id, prompt_name, and _model_obj are not updated here
            # because they are not included in the API response. They remain as set during __init__()
            # Note: model_alias is not in the create response, but is extracted when retrieving/refreshing
            self.id = created_experiment.id
            self.name = created_experiment.name
            self.created_at = created_experiment.created_at
            self.updated_at = created_experiment.updated_at
            self.additional_properties = created_experiment.additional_properties
            self._experiment_response = created_experiment

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            _logger.info(f"Experiment.create: id='{self.id}' - completed")
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            _logger.error(f"Experiment.create: name='{self.name}' - failed: {e}")
            raise

    @classmethod
    def _create_empty(cls) -> Experiment:
        """Internal constructor bypassing __init__ for API hydration."""
        instance = cls.__new__(cls)
        super(Experiment, instance).__init__()
        # Initialize all required attributes
        instance.name = ""
        instance.project_id = None
        instance.project_name = None
        instance.id = None
        instance.created_at = None
        instance.updated_at = None
        instance.additional_properties = {}
        instance.metrics = None
        # TODO: Function-based experiments temporarily disabled - need to validate implementation
        # instance.function = None
        instance.prompt_settings = None
        instance.model_alias = None
        instance.dataset_id = None
        instance.dataset_name = None
        instance.prompt_id = None
        instance.prompt_name = None
        instance._dataset_obj = None
        instance._prompt_template = None
        instance._model_obj = None
        instance._experiment_response = None
        instance._job_id = None
        return instance

    @classmethod
    def _from_api_response(cls, retrieved_experiment: ExperimentResponse) -> Experiment:
        """
        Factory method to create an Experiment instance from an API response.

        Args:
            retrieved_experiment: The experiment data retrieved from the API.

        Returns
        -------
            Experiment: A new Experiment instance populated with the API data.
        """
        # TODO: Fix serialization
        instance = cls._create_empty()
        instance.id = retrieved_experiment.id
        instance.name = getattr(retrieved_experiment, "name", "")
        instance.created_at = getattr(retrieved_experiment, "created_at", None)
        instance.updated_at = getattr(retrieved_experiment, "updated_at", None)
        instance.additional_properties = getattr(retrieved_experiment, "additional_properties", {})
        instance.project_id = None  # Will be set by caller
        instance.project_name = None  # Will be set by caller

        # Extract dataset info from nested ExperimentDataset object
        dataset_api = getattr(retrieved_experiment, "dataset", None)
        if dataset_api is not None and not isinstance(dataset_api, Unset):
            instance.dataset_id = getattr(dataset_api, "dataset_id", None)
            if isinstance(instance.dataset_id, Unset):
                instance.dataset_id = None
            instance.dataset_name = getattr(dataset_api, "name", None)
            if isinstance(instance.dataset_name, Unset):
                instance.dataset_name = None
        else:
            instance.dataset_id = None
            instance.dataset_name = None

        # Extract prompt info from nested ExperimentPrompt object
        prompt_api = getattr(retrieved_experiment, "prompt", None)
        _logger.debug(f"Experiment._from_api_response: raw prompt_api value: {prompt_api}, type: {type(prompt_api)}")

        if prompt_api is not None and not isinstance(prompt_api, Unset):
            instance.prompt_id = getattr(prompt_api, "prompt_template_id", None)
            if isinstance(instance.prompt_id, Unset):
                instance.prompt_id = None
            instance.prompt_name = getattr(prompt_api, "name", None)
            if isinstance(instance.prompt_name, Unset):
                instance.prompt_name = None
            _logger.debug(
                f"Experiment._from_api_response: Extracted prompt_id='{instance.prompt_id}', prompt_name='{instance.prompt_name}'"
            )
        else:
            instance.prompt_id = None
            instance.prompt_name = None
            _logger.warning(
                f"Experiment._from_api_response: id='{instance.id}' - No prompt information in API response. "
                f"prompt_api is {'None' if prompt_api is None else 'Unset'}"
            )

        _logger.debug(
            f"Experiment._from_api_response: id='{instance.id}' "
            f"dataset_id='{instance.dataset_id}' dataset_name='{instance.dataset_name}' "
            f"prompt_id='{instance.prompt_id}' prompt_name='{instance.prompt_name}'"
        )

        # Extract prompt settings if available
        prompt_settings_api = getattr(retrieved_experiment, "prompt_run_settings", None)
        if prompt_settings_api is not None and not isinstance(prompt_settings_api, Unset):
            instance.prompt_settings = prompt_settings_api
            # Extract model_alias from prompt_settings if available
            model_alias_from_settings = getattr(prompt_settings_api, "model_alias", None)
            if model_alias_from_settings is not None and not isinstance(model_alias_from_settings, Unset):
                instance.model_alias = model_alias_from_settings
        else:
            instance.prompt_settings = None

        # Also check for prompt_model field (alternative source for model info)
        if instance.model_alias is None:
            prompt_model_api = getattr(retrieved_experiment, "prompt_model", None)
            if prompt_model_api is not None and not isinstance(prompt_model_api, Unset):
                instance.model_alias = prompt_model_api

        instance.metrics = None
        # TODO: Function-based experiments temporarily disabled - need to validate implementation
        # instance.function = None
        instance._dataset_obj = None
        instance._prompt_template = None
        instance._model_obj = None
        instance._experiment_response = retrieved_experiment
        instance._job_id = None
        # Set state to synced since we just retrieved from API
        instance._set_state(SyncState.SYNCED)
        return instance

    @classmethod
    @require_exactly_one("project_id", "project_name")
    def get(cls, *, name: str, project_id: str | None = None, project_name: str | None = None) -> Experiment | None:
        """
        Get an existing experiment by name.

        Args:
            name (str): The experiment name.
            project_id (Optional[str]): The project ID.
            project_name (Optional[str]): The project name.

        Returns
        -------
            Optional[Experiment]: The experiment if found, None otherwise.

        Raises
        ------
            ValidationError: If neither or both project_id and project_name are provided.
            ValueError: If the project cannot be found.

        Examples
        --------
            # Get by project name
            experiment = Experiment.get(
                name="ml-evaluation",
                project_name="My AI Project"
            )

            # Get by project ID
            experiment = Experiment.get(
                name="ml-evaluation",
                project_id="project-123"
            )
        """
        # Resolve project (prefer ID over name since get_with_env_fallbacks requires exactly one)
        project_obj = Projects().get_with_env_fallbacks(
            id=project_id if project_id else None, name=project_name if not project_id else None
        )
        if not project_obj:
            raise ValueError(f"Project not found: id={project_id}, name={project_name}")

        experiments_service = ExperimentsService()
        retrieved_experiment = experiments_service.get(project_id=project_obj.id, experiment_name=name)

        if retrieved_experiment is None:
            return None

        instance = cls._from_api_response(retrieved_experiment)
        instance.project_id = project_obj.id
        instance.project_name = project_obj.name
        return instance

    @classmethod
    @require_exactly_one("project_id", "project_name")
    def list(cls, *, project_id: str | None = None, project_name: str | None = None) -> list[Experiment]:
        """
        List all experiments for a project.

        Args:
            project_id (Optional[str]): The project ID.
            project_name (Optional[str]): The project name.

        Returns
        -------
            List[Experiment]: A list of experiments for the project.

        Raises
        ------
            ValidationError: If neither or both project_id and project_name are provided.
            ValueError: If the project cannot be found.

        Examples
        --------
            # List by project name
            experiments = Experiment.list(project_name="My AI Project")

            # List by project ID
            experiments = Experiment.list(project_id="project-123")
        """
        # Resolve project (prefer ID over name since get_with_env_fallbacks requires exactly one)
        project_obj = Projects().get_with_env_fallbacks(
            id=project_id if project_id else None, name=project_name if not project_id else None
        )
        if not project_obj:
            raise ValueError(f"Project not found: id={project_id}, name={project_name}")

        experiments_service = ExperimentsService()
        retrieved_experiments = experiments_service.list(project_id=project_obj.id)

        if retrieved_experiments is None or isinstance(retrieved_experiments, HTTPValidationError):
            return []

        instances = [cls._from_api_response(exp) for exp in retrieved_experiments]
        # Set project info for all instances
        for instance in instances:
            instance.project_id = project_obj.id
            instance.project_name = project_obj.name
        return instances

    def refresh(self) -> None:
        """
        Refresh this experiment's state from the API.

        Updates all attributes with the latest values from the remote API
        and sets the state to SYNCED.

        Raises
        ------
            ValueError: If the experiment ID or project_id is not set.
            Exception: If the API call fails or the experiment no longer exists.

        Examples
        --------
            experiment.refresh()
            assert experiment.is_synced()
        """
        if self.id is None:
            raise ValueError("Experiment ID is not set. Cannot refresh a local-only experiment.")

        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot refresh experiment without project_id.")

        try:
            _logger.debug(f"Experiment.refresh: id='{self.id}' - started")
            experiments_service = ExperimentsService()
            retrieved_experiment = experiments_service.get(project_id=self.project_id, experiment_name=self.name)

            if retrieved_experiment is None:
                raise ValueError(f"Experiment with id '{self.id}' no longer exists")

            # Update all top-level attributes from response
            self.id = retrieved_experiment.id
            self.name = retrieved_experiment.name
            self.created_at = retrieved_experiment.created_at
            self.updated_at = retrieved_experiment.updated_at
            self.additional_properties = retrieved_experiment.additional_properties

            # Extract and update dataset info from nested ExperimentDataset object
            dataset_api = getattr(retrieved_experiment, "dataset", None)
            if dataset_api is not None and not isinstance(dataset_api, Unset):
                self.dataset_id = getattr(dataset_api, "dataset_id", None)
                if isinstance(self.dataset_id, Unset):
                    self.dataset_id = None
                self.dataset_name = getattr(dataset_api, "name", None)
                if isinstance(self.dataset_name, Unset):
                    self.dataset_name = None
            else:
                self.dataset_id = None
                self.dataset_name = None

            # Extract and update prompt info from nested ExperimentPrompt object
            # Preserve locally-set values if API doesn't have them
            saved_prompt_id = self.prompt_id
            saved_prompt_name = self.prompt_name

            prompt_api = getattr(retrieved_experiment, "prompt", None)
            if prompt_api is not None and not isinstance(prompt_api, Unset):
                self.prompt_id = getattr(prompt_api, "prompt_template_id", None)
                if isinstance(self.prompt_id, Unset):
                    self.prompt_id = None
                self.prompt_name = getattr(prompt_api, "name", None)
                if isinstance(self.prompt_name, Unset):
                    self.prompt_name = None
            else:
                # Preserve locally-set values if API doesn't have prompt info
                self.prompt_id = saved_prompt_id
                self.prompt_name = saved_prompt_name

            # Extract and update prompt settings if available
            # Always reset model_alias and _model_obj first to avoid stale values
            self.model_alias = None
            self._model_obj = None

            prompt_settings_api = getattr(retrieved_experiment, "prompt_run_settings", None)
            if prompt_settings_api is not None and not isinstance(prompt_settings_api, Unset):
                self.prompt_settings = prompt_settings_api
                # Extract model_alias from prompt_settings if available
                model_alias_from_settings = getattr(prompt_settings_api, "model_alias", None)
                if model_alias_from_settings is not None and not isinstance(model_alias_from_settings, Unset):
                    self.model_alias = model_alias_from_settings
            else:
                self.prompt_settings = None

            # Also check for prompt_model field (alternative source for model info)
            # Only update if we haven't already set it from prompt_settings
            if self.model_alias is None:
                prompt_model_api = getattr(retrieved_experiment, "prompt_model", None)
                if prompt_model_api is not None and not isinstance(prompt_model_api, Unset):
                    self.model_alias = prompt_model_api

            # Update the cached API response
            self._experiment_response = retrieved_experiment

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            _logger.debug(f"Experiment.refresh: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            _logger.error(f"Experiment.refresh: id='{self.id}' - failed: {e}")
            raise

    def delete(self) -> None:
        """
        Delete this experiment.

        This is a destructive operation that permanently removes the experiment
        and all associated data (traces, spans, metrics, results) from the API.

        WARNING: This operation cannot be undone!

        After successful deletion, the object state is set to DELETED. The local
        object still exists in memory but no longer represents a remote resource.

        Raises
        ------
            ValueError: If the experiment ID or project_id is not set.
            Exception: If the API call fails.

        Examples
        --------
            # Delete an experiment
            experiment = Experiment.get(
                name="old-experiment",
                project_name="My AI Project"
            )
            experiment.delete()
            assert experiment.is_deleted()

            # After deletion, the experiment no longer exists remotely
            # The local object is marked as DELETED
            print(experiment.sync_state)  # SyncState.DELETED
        """
        if self.id is None:
            raise ValueError("Experiment ID is not set. Cannot delete a local-only experiment.")

        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot delete experiment without project_id.")

        try:
            _logger.info(f"Experiment.delete: id='{self.id}' name='{self.name}' - started")

            config = GalileoPythonConfig.get()
            result = delete_experiment_projects_project_id_experiments_experiment_id_delete.sync(
                project_id=self.project_id, experiment_id=self.id, client=config.api_client
            )

            # Check for validation errors
            if isinstance(result, HTTPValidationError):
                raise ValueError(f"Failed to delete experiment: {result.detail}")

            # Set state to deleted after successful deletion
            self._set_state(SyncState.DELETED)
            _logger.info(f"Experiment.delete: id='{self.id}' name='{self.name}' - completed")

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            _logger.error(f"Experiment.delete: id='{self.id}' name='{self.name}' - failed: {e}")
            raise

    @require_exactly_one("prompt", "prompt_name", "prompt_id")
    def set_prompt(
        self,
        *,
        prompt: Prompt | PromptTemplate | str | None = None,
        prompt_name: str | None = None,
        prompt_id: str | None = None,
    ) -> None:
        """
        Set or update the prompt for this experiment.

        This is useful for experiments created in the playground where prompt information
        may not be automatically retrieved from the API.

        Args:
            prompt: Prompt object, prompt name, or PromptTemplate object.
            prompt_name: Name of the prompt template (alternative to prompt parameter).
            prompt_id: ID of the prompt template (alternative to prompt parameter).

        Raises
        ------
            ValueError: If no prompt information is provided.

        Examples
        --------
            # Set prompt by name
            experiment.set_prompt(prompt_name="my-prompt")

            # Set prompt by ID
            experiment.set_prompt(prompt_id="prompt-123")

            # Set prompt using Prompt object
            from galileo.__future__ import Prompt
            prompt = Prompt.get(name="my-prompt")
            experiment.set_prompt(prompt=prompt)

            # Set prompt using string (treated as name)
            experiment.set_prompt(prompt="my-prompt")
        """
        # Reset prompt state
        self.prompt_id = None
        self.prompt_name = None
        self._prompt_template = None

        # TODO: Fix serialization
        # Handle prompt parameter
        if prompt is not None:
            # Local import to avoid circular dependency
            from galileo.__future__.prompt import Prompt

            if isinstance(prompt, Prompt):
                self.prompt_id = prompt.id
                self.prompt_name = prompt.name
            elif isinstance(prompt, PromptTemplate):
                self._prompt_template = prompt
                self.prompt_id = prompt.selected_version_id
                self.prompt_name = prompt.name
            elif isinstance(prompt, str):
                self.prompt_name = prompt
        elif prompt_name is not None:
            self.prompt_name = prompt_name
        elif prompt_id is not None:
            self.prompt_id = prompt_id

        _logger.info(
            f"Experiment.set_prompt: id='{self.id}' prompt_name='{self.prompt_name}' prompt_id='{self.prompt_id}'"
        )

    def get_prompt_template_settings(self) -> PromptRunSettings | None:
        """
        Get the settings from the associated prompt template.

        WARNING: These settings are NOT automatically used when running the experiment.
        The Runners service ignores template settings and only uses the prompt_settings
        passed to the run() method. Use this method to retrieve template settings if
        you want to apply them to the job.

        Returns
        -------
            PromptRunSettings | None: Settings from the template, or None if no template or no settings.

        Examples
        --------
            experiment = Experiment(
                name="ml-evaluation",
                prompt_name="ml-prompt",
                dataset_name="ml-dataset",
                project_name="My Project"
            ).create()

            # Get settings from template
            template_settings = experiment.get_prompt_template_settings()

            # Note: Current run() doesn't accept prompt_settings parameter
            # This would require updating the run() signature
        """
        if self._prompt_template is None:
            if self.prompt_id:
                self._prompt_template = get_prompt(id=self.prompt_id)
            elif self.prompt_name:
                self._prompt_template = get_prompt(name=self.prompt_name)

        if self._prompt_template is None:
            return None

        # Check if the template has settings
        # TODO: Move this to a serializer.
        if hasattr(self._prompt_template, "selected_version"):
            selected_version = getattr(self._prompt_template, "selected_version", None)
            if selected_version and hasattr(selected_version, "settings"):
                settings = getattr(selected_version, "settings", None)
                if settings and not isinstance(settings, Unset):
                    return settings

        return None

    def has_traces(self) -> bool:
        """
        Check if this experiment has any traces.

        Experiments with traces cannot have new jobs created on them.
        To re-run an experiment, create a new experiment with a different name.

        Returns
        -------
            bool: True if the experiment has traces, False otherwise.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My Project")
            if experiment.has_traces():
                print("This experiment has already been run")
                # Create a new one for re-run
                new_exp = Experiment(
                    name=f"{experiment.name}-rerun-1",
                    dataset_name=experiment.dataset_name,
                    prompt_name=experiment.prompt_name,
                    project_name=experiment.project_name
                ).create()
        """
        if self.id is None or self.project_id is None:
            return False

        # Query for traces with limit=1 to check existence
        try:
            result = self.query(record_type=RecordType.TRACE, limit=1)
            return len(result) > 0
        except Exception:
            # If query fails, assume no traces (fail open)
            return False

    def run(self) -> ExperimentRunResult:
        """
        Execute this experiment.

        Currently supports running experiments with a prompt template and dataset.

        Note: Function-based experiments are temporarily disabled pending validation.

        Returns
        -------
            ExperimentRunResult: Result object with:
                - link: URL to view results in console
                - message: Status message
                - status: ExperimentStatusInfo with progress details
                - experiment_id, project_id: IDs
                - dataset_info, prompt_info: Associated resource info

        Raises
        ------
            ValueError: If required parameters are missing or invalid.

        Examples
        --------
            # Run an experiment with prompt template
            experiment = Experiment(
                name="ml-evaluation",
                dataset_name="ml-dataset",
                prompt_name="ml-prompt",
                metrics=["correctness", "completeness"],
                project_name="My AI Project"
            ).create()

            result = experiment.run()
            print(result.link)  # URL to results
            print(result.status)  # Human-readable status
            print(f"Progress: {result.status.overall_progress}%")
        """
        if self.id is None:
            raise ValueError("Experiment must be created before running. Call .create() first.")

        if not self.project_id:
            raise ValueError("Project ID is not set. Cannot run experiment without project_id.")

        # Check if experiment already has traces (immutability constraint)
        if self.has_traces():
            raise ValueError(
                f"Cannot run experiment '{self.name}' - it already has traces from a previous run.\n\n"
                "Experiments are immutable after execution. To re-run with the same configuration:\n"
                "1. Create a new experiment with a different name\n"
                "2. Use the same dataset, prompt, and metrics\n\n"
                "Example:\n"
                f"  new_experiment = Experiment(\n"
                f"      name='{self.name}-rerun-1',\n"
                f"      dataset_name='{self.dataset_name}',\n"
                f"      prompt_name='{self.prompt_name}',\n"
                f"      metrics={self.metrics},\n"
                f"      project_name='{self.project_name}'\n"
                "  ).create().run()"
            )

        # Validate dataset requirement for prompt template experiments
        # Check if we have or will have a prompt template (need to check before loading)
        has_prompt_template = (
            self._prompt_template is not None or self.prompt_id is not None or self.prompt_name is not None
        )

        if has_prompt_template and not self.dataset_id and not self.dataset_name and self._dataset_obj is None:
            raise ValueError("A dataset must be provided when running an experiment with a prompt template.")

        try:
            _logger.info(f"Experiment.run: id='{self.id}' name='{self.name}' - started")

            # Resolve project (prefer ID over name since get_with_env_fallbacks requires exactly one)
            project_obj = Projects().get_with_env_fallbacks(
                id=self.project_id if self.project_id else None, name=self.project_name if not self.project_id else None
            )
            if not project_obj:
                raise ValueError(f"Project not found: id={self.project_id}, name={self.project_name}")

            # Load dataset and records (use cached if available)
            dataset_obj: LegacyDataset | None
            # TODO: records variable needed when function-based experiments are re-enabled
            # records: list[DatasetRecord]

            if self._dataset_obj is not None:
                dataset_obj = self._dataset_obj
                # TODO: records needed for function-based experiments
                # records = get_records_for_dataset(self._dataset_obj)
            elif self.dataset_id or self.dataset_name:
                dataset_obj, _records = load_dataset_and_records(
                    dataset=self.dataset_name or self.dataset_id,
                    dataset_id=self.dataset_id,
                    dataset_name=self.dataset_name,
                )
                # TODO: records needed for function-based experiments
                # records = _records
            else:
                dataset_obj = None
                # TODO: records needed for function-based experiments
                # records = []

            # Validate experiment configuration
            if self._prompt_template and not dataset_obj:
                raise ValueError("A dataset must be provided when a prompt_template is used")

            # TODO: Function-based experiments temporarily disabled - need to validate implementation
            # The logic below needs to be re-enabled after validating the functionality.
            #
            # if self.function and not records:
            #     raise ValueError("A dataset or list of records must be provided when a function is used")
            #
            # if self.function and self._prompt_template:
            #     raise ValueError("A function or prompt_template should be provided, but not both")

            # Set up metrics if provided
            scorer_settings: list[ScorerConfig] | None = None
            local_metrics: list[LocalMetricConfig] = []
            if self.metrics is not None:
                scorer_settings, local_metrics = create_metric_configs(project_obj.id, self.id, self.metrics)

            experiments_service = ExperimentsService()

            # TODO: Function-based experiment execution temporarily disabled - need to validate implementation
            # Execute a runner function experiment
            # if self.function is not None:
            #     result = experiments_service.run_with_function(
            #         project_obj=project_obj,
            #         experiment_obj=self._experiment_response,
            #         records=records,
            #         func=self.function,
            #         local_metrics=local_metrics,
            #     )
            #     _logger.info(f"Experiment.run: id='{self.id}' - completed")
            #     return ExperimentRunResult(result)

            # Load prompt template if needed
            if self._prompt_template is None:
                _logger.debug(
                    f"Experiment.run: id='{self.id}' - Loading prompt template: "
                    f"prompt_id='{self.prompt_id}', prompt_name='{self.prompt_name}'"
                )
                if self.prompt_id:
                    _logger.debug(f"Experiment.run: id='{self.id}' - Loading prompt by ID: {self.prompt_id}")
                    self._prompt_template = get_prompt(id=self.prompt_id)
                    _logger.debug(
                        f"Experiment.run: id='{self.id}' - Loaded prompt template: {self._prompt_template is not None}"
                    )
                elif self.prompt_name:
                    _logger.debug(f"Experiment.run: id='{self.id}' - Loading prompt by name: {self.prompt_name}")
                    self._prompt_template = get_prompt(name=self.prompt_name)
                    _logger.debug(
                        f"Experiment.run: id='{self.id}' - Loaded prompt template: {self._prompt_template is not None}"
                    )

            if self._prompt_template is None:
                # Check if this is a playground experiment
                playground_info = ""
                if self._experiment_response and hasattr(self._experiment_response, "playground"):
                    playground = getattr(self._experiment_response, "playground", None)
                    if playground and not isinstance(playground, Unset):
                        playground_name = getattr(playground, "name", None)
                        if playground_name:
                            playground_info = (
                                f"This experiment was created from playground '{playground_name}'. "
                                "The prompt used in that playground is not automatically linked to this experiment."
                            )

                # Show debug info about what was attempted
                debug_info = (
                    f"\n\nDebug info:\n"
                    f"  prompt_id: {self.prompt_id}\n"
                    f"  prompt_name: {self.prompt_name}\n"
                    f"  _prompt_template: {self._prompt_template}\n"
                )

                error_msg = (
                    "A prompt template must be provided to run this experiment. "
                    f"{playground_info}\n\n"
                    "Please set the prompt before running:\n\n"
                    "  experiment.set_prompt(prompt_name='your-prompt-name')\n"
                    "  # or\n"
                    "  experiment.set_prompt(prompt_id='your-prompt-id')\n"
                    "  # or\n"
                    "  from galileo.__future__ import Prompt\n"
                    "  experiment.set_prompt(prompt=Prompt.get(name='your-prompt-name'))\n\n"
                    "Then call experiment.run() again."
                    f"{debug_info}"
                )
                raise ValueError(error_msg)

            if dataset_obj is None:
                raise ValueError("A dataset object must be provided")

            if local_metrics:
                raise ValueError(
                    "Local metrics can only be used with a locally run experiment, not a prompt experiment."
                )

            # Determine effective prompt settings
            # Priority: 1. explicit prompt_settings, 2. model parameter, 3. None
            effective_prompt_settings = self.prompt_settings

            if self.model_alias:
                if effective_prompt_settings is None:
                    # Create default settings with the specified model
                    effective_prompt_settings = PromptRunSettings(model_alias=self.model_alias)
                    _logger.debug(
                        f"Experiment.run: id='{self.id}' - Using model '{self.model_alias}' "
                        "from model parameter (no prompt_settings provided)"
                    )
                else:
                    # Override model in provided settings
                    _logger.debug(
                        f"Experiment.run: id='{self.id}' - Overriding model in prompt_settings "
                        f"with '{self.model_alias}' from model parameter"
                    )
                    # Create a new PromptRunSettings with the model override
                    settings_dict = (
                        effective_prompt_settings.to_dict() if hasattr(effective_prompt_settings, "to_dict") else {}
                    )
                    settings_dict["model_alias"] = self.model_alias
                    effective_prompt_settings = PromptRunSettings(**settings_dict)

            # Execute a prompt template experiment
            result = experiments_service.run(
                project_obj,
                self._experiment_response,
                self._prompt_template,
                dataset_obj.dataset.id,
                scorer_settings,
                effective_prompt_settings,
            )

            # Store job ID for monitoring if available
            # Note: The job ID would need to be extracted from the result or stored separately

            _logger.info(f"Experiment.run: id='{self.id}' - completed")
            return ExperimentRunResult(result)

        except Exception as e:
            _logger.error(f"Experiment.run: id='{self.id}' - failed: {e}")
            raise

    def get_status(self) -> ExperimentStatusInfo:
        """
        Get the current status of this experiment in human-readable format.

        Returns
        -------
            ExperimentStatusInfo: Detailed status information including progress and phases.

        Raises
        ------
            ValueError: If the experiment lacks required id or project_id attributes.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")
            status = experiment.get_status()

            print(status)  # Human-readable status
            print(f"Progress: {status.overall_progress}%")

            if status.is_complete:
                print("Experiment completed!")
            elif status.is_in_progress:
                print(f"Running: {status.log_generation}")
        """
        if self.id is None:
            raise ValueError("Experiment ID is not set. Cannot get status for a local-only experiment.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot get status without project_id.")

        # Refresh to get latest status
        self.refresh()

        if self._experiment_response is None:
            raise ValueError("Experiment response not available. Try calling refresh() first.")

        return ExperimentStatusInfo(self._experiment_response)

    def monitor_progress(self, job_id: str | None = None) -> str:
        """
        Monitor the progress of the experiment job with a progress bar.

        Args:
            job_id: Optional job ID to monitor. If not provided, will attempt to find
                   the primary job for this experiment.

        Returns
        -------
            str: The unique identifier of the completed job.

        Raises
        ------
            ValueError: If the experiment lacks required id or project_id attributes,
                       or if no job_id is provided and no job can be found.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")
            result = experiment.run()

            # Monitor the job progress
            completed_job_id = experiment.monitor_progress()
        """
        if self.id is None:
            raise ValueError("Experiment ID is not set. Cannot monitor progress for a local-only experiment.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot monitor progress without project_id.")

        if job_id is None:
            # Try to get job from stored state or query for it
            if self._job_id:
                job_id = self._job_id
            else:
                # Get the first scorer job
                scorer_jobs = get_run_scorer_jobs(project_id=self.project_id, run_id=self.id)
                if not scorer_jobs:
                    raise ValueError("No job found for this experiment. Run the experiment first.")
                job_id = str(scorer_jobs[0].id)

        _logger.info(f"Experiment.monitor_progress: experiment_id='{self.id}' job_id='{job_id}' - started")

        # Monitor job progress with progress bar
        completed_job_id = job_progress(job_id=job_id, project_id=self.project_id, run_id=self.id)

        _logger.info(f"Experiment.monitor_progress: experiment_id='{self.id}' - completed")
        return str(completed_job_id)

    # Query and export methods - similar to LogStream

    def query(
        self,
        record_type: RecordType,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> QueryResult:
        """
        Query records in this experiment.

        This method provides a convenient way to search spans, traces, or sessions
        within the current experiment results.

        Args:
            record_type: The type of records to query (SPAN, TRACE, or SESSION).
            filters: A list of filters to apply to the query.
            sort: A sort clause to order the query results.
            limit: The maximum number of records to return.
            starting_token: The token for the next page of results.

        Returns
        -------
            QueryResult: A list-like object containing the query results with pagination support.

        Raises
        ------
            ValueError: If the experiment lacks required id or project_id attributes.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")

            # Query experiment results
            results = experiment.query(
                record_type=RecordType.TRACE,
                filters=[
                    experiment.trace_columns["input"].contains("machine learning"),
                    experiment.trace_columns["metrics/correctness"].greater_than(0.8)
                ],
                sort=experiment.trace_columns["created_at"].descending(),
                limit=50
            )

            for record in results:
                print(record["id"], record["input"])
        """
        if self.id is None:
            raise ValueError("Experiment ID is not set. Cannot query a local-only experiment.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot query experiment without project_id.")

        _logger.debug(f"Experiment.query: id='{self.id}' record_type='{record_type.value}' limit={limit} - started")

        # Capture project_id and experiment_id (run_id) for use in pagination function
        project_id = self.project_id
        experiment_id = self.id

        search_service = Search()
        response = search_service.query(
            project_id=project_id,
            record_type=record_type,
            experiment_id=experiment_id,  # Use experiment_id for experiments (not log_stream_id)
            filters=filters,
            sort=sort,
            limit=limit,
            starting_token=starting_token,
        )

        # Create a query function that returns raw response for pagination
        def query_fn(
            record_type: RecordType,
            filters: builtins.list[FilterType] | None,
            sort: LogRecordsSortClause | None,
            limit: int,
            starting_token: int,
        ) -> Any:
            return Search().query(
                project_id=project_id,
                record_type=record_type,
                experiment_id=experiment_id,
                filters=filters,
                sort=sort,
                limit=limit,
                starting_token=starting_token,
            )

        # Wrap the response in QueryResult for easy access and pagination
        return QueryResult(response=response, query_fn=query_fn, record_type=record_type, filters=filters, sort=sort)

    def get_spans(
        self,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> QueryResult:
        """
        Query spans in this experiment.

        This is a convenience method that queries for spans specifically.

        Args:
            filters: A list of filters to apply to the query.
            sort: A sort clause to order the query results.
            limit: The maximum number of records to return.
            starting_token: The token for the next page of results.

        Returns
        -------
            QueryResult: A list-like object containing the span query results with pagination support.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")
            spans = experiment.get_spans(
                filters=[experiment.span_columns["input"].contains("world")],
                sort=experiment.span_columns["created_at"].descending(),
                limit=50
            )
        """
        _logger.debug(f"Experiment.get_spans: id='{self.id}' limit={limit} - started")
        return self.query(
            record_type=RecordType.SPAN, filters=filters, sort=sort, limit=limit, starting_token=starting_token
        )

    def get_traces(
        self,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> QueryResult:
        """
        Query traces in this experiment.

        This is a convenience method that queries for traces specifically.

        Args:
            filters: A list of filters to apply to the query.
            sort: A sort clause to order the query results.
            limit: The maximum number of records to return.
            starting_token: The token for the next page of results.

        Returns
        -------
            QueryResult: A list-like object containing the trace query results with pagination support.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")
            traces = experiment.get_traces(
                filters=[experiment.trace_columns["input"].contains("largest")],
                sort=experiment.trace_columns["created_at"].descending(),
                limit=50
            )
        """
        _logger.debug(f"Experiment.get_traces: id='{self.id}' limit={limit} - started")
        return self.query(
            record_type=RecordType.TRACE, filters=filters, sort=sort, limit=limit, starting_token=starting_token
        )

    def get_sessions(
        self,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
        limit: int = 100,
        starting_token: int = 0,
    ) -> QueryResult:
        """
        Query sessions in this experiment.

        This is a convenience method that queries for sessions specifically.

        Args:
            filters: A list of filters to apply to the query.
            sort: A sort clause to order the query results.
            limit: The maximum number of records to return.
            starting_token: The token for the next page of results.

        Returns
        -------
            QueryResult: A list-like object containing the session query results with pagination support.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")
            sessions = experiment.get_sessions(
                filters=[experiment.session_columns["model"].equals("gpt-4o-mini")],
                sort=experiment.session_columns["created_at"].descending(),
                limit=50
            )
        """
        _logger.debug(f"Experiment.get_sessions: id='{self.id}' limit={limit} - started")
        return self.query(
            record_type=RecordType.SESSION, filters=filters, sort=sort, limit=limit, starting_token=starting_token
        )

    def export_records(
        self,
        record_type: RecordType = RecordType.TRACE,
        filters: builtins.list[FilterType] | None = None,
        sort: LogRecordsSortClause = LogRecordsSortClause(column_id="created_at", ascending=False),
        export_format: LLMExportFormat = LLMExportFormat.JSONL,
        column_ids: builtins.list[str] | None = None,
        redact: bool = True,
    ) -> Iterator[dict[str, Any]]:
        """
        Export records from this experiment.

        Args:
            record_type: The type of records to export (SPAN, TRACE, or SESSION).
            filters: A list of filters to apply to the export.
            sort: A sort clause to order the exported records.
            export_format: The desired format for the exported data.
            column_ids: A list of column IDs to include in the export.
            redact: Redact sensitive data from the response.

        Returns
        -------
            Iterator[dict[str, Any]]: An iterator that yields each record as a dictionary.

        Raises
        ------
            ValueError: If the experiment lacks required id or project_id attributes.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")

            for record in experiment.export_records(
                record_type=RecordType.TRACE,
                filters=[experiment.trace_columns["metrics/correctness"].greater_than(0.8)],
                sort=experiment.trace_columns["created_at"].descending()
            ):
                print(record)
        """
        if self.id is None:
            raise ValueError("Experiment ID is not set. Cannot export from a local-only experiment.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot export experiment without project_id.")

        # Convert RecordType to RootType for the export client
        root_type = RECORD_TYPE_TO_ROOT_TYPE[record_type]

        _logger.info(
            f"Experiment.export_records: id='{self.id}' record_type='{record_type.value}' "
            f"export_format='{export_format.value}' - started"
        )

        export_client = ExportClient()
        return export_client.records(
            project_id=self.project_id,
            root_type=root_type,
            filters=filters,
            sort=sort,
            export_format=export_format,
            log_stream_id=self.id,  # Experiments use log_stream_id param for run_id
            column_ids=column_ids,
            redact=redact,
        )

    def _get_columns(self, api_func: Any, error_msg: str) -> LogRecordsAvailableColumnsResponse:
        """Helper method to retrieve available columns from the API."""
        if self.id is None:
            raise ValueError("Experiment ID is not set. Cannot get columns from a local-only experiment.")
        if self.project_id is None:
            raise ValueError("Project ID is not set. Cannot get columns without project_id.")

        config = GalileoPythonConfig.get()
        body = LogRecordsAvailableColumnsRequest(log_stream_id=self.id)
        response = api_func.sync(project_id=self.project_id, client=config.api_client, body=body)
        if isinstance(response, HTTPValidationError):
            raise response
        if not response:
            raise ValueError(error_msg)
        return response

    @property
    def project(self) -> Project | None:
        """Get the project this experiment belongs to."""
        # Local import to avoid circular dependency
        from galileo.__future__.project import Project

        return Project.get(id=self.project_id)

    @property
    def dataset(self) -> Dataset | None:
        """Get the dataset associated with this experiment."""
        if self.dataset_id is None and self.dataset_name is None:
            return None
        # Local import to avoid circular dependency
        from galileo.__future__.dataset import Dataset

        if self.dataset_id:
            return Dataset.get(id=self.dataset_id)
        return Dataset.get(name=self.dataset_name)

    @property
    def prompt(self) -> Prompt | None:
        """
        Get the prompt template associated with this experiment.

        Note: For playground-created experiments that haven't been run yet,
        the prompt information may not be available automatically. In such cases,
        use set_prompt() to manually set the prompt before running the experiment.
        """
        if self.prompt_id is None and self.prompt_name is None:
            return None
        # Local import to avoid circular dependency
        from galileo.__future__.prompt import Prompt

        if self.prompt_id:
            return Prompt.get(id=self.prompt_id)
        return Prompt.get(name=self.prompt_name)

    @property
    def playground_name(self) -> str | None:
        """
        Get the name of the playground this experiment was created from, if any.

        Returns
        -------
            str | None: Playground name if this is a playground experiment, None otherwise.
        """
        if self._experiment_response and hasattr(self._experiment_response, "playground"):
            playground = getattr(self._experiment_response, "playground", None)
            if playground and not isinstance(playground, Unset):
                return getattr(playground, "name", None)
        return None

    @property
    def aggregate_metrics(self) -> dict[str, float] | None:
        """
        Get computed aggregate metrics for this experiment.

        Returns aggregate metrics like average_cost, average_latency, total_responses,
        and quality metrics (e.g., average_factuality, average_correctness).

        Note: Call refresh() first to get the latest metric values after experiment completion.

        Returns
        -------
            dict[str, float] | None: Dictionary of metric names to values, or None if not available.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My Project")
            experiment.refresh()

            metrics = experiment.aggregate_metrics
            if metrics:
                print(f"Average cost: ${metrics.get('average_cost', 0):.4f}")
                print(f"Total responses: {metrics.get('total_responses', 0)}")
                print(f"Average latency: {metrics.get('average_latency', 0):.2f}ms")

                # Quality metrics (if configured)
                if 'average_correctness' in metrics:
                    print(f"Average correctness: {metrics['average_correctness']:.2%}")
        """
        if self._experiment_response is None:
            return None

        agg_metrics = getattr(self._experiment_response, "aggregate_metrics", None)

        if agg_metrics is None or isinstance(agg_metrics, Unset):
            return None

        # Convert to regular dict for easier use
        if hasattr(agg_metrics, "to_dict"):
            return agg_metrics.to_dict()

        # Handle if it's already a dict-like object
        try:
            return dict(agg_metrics) if agg_metrics else None
        except (TypeError, ValueError):
            return None

    @property
    def tags(self) -> dict[str, builtins.list[dict]] | None:
        """
        Get tags associated with this experiment.

        Tags are organized by category (e.g., "generic", "rag"). Each category
        contains a list of tag objects with key, value, and metadata.

        Returns
        -------
            dict[str, list[dict]] | None: Dictionary of tag categories, or None if not available.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My Project")
            tags = experiment.tags

            if tags and 'generic' in tags:
                for tag in tags['generic']:
                    print(f"{tag['key']}={tag['value']}")
        """
        if self._experiment_response is None:
            return None

        tags = getattr(self._experiment_response, "tags", None)
        if tags is None or isinstance(tags, Unset):
            return None

        # Convert to regular dict if it has to_dict method
        if hasattr(tags, "to_dict"):
            return tags.to_dict()

        # If it's already a dict-like object with attributes, extract them
        if hasattr(tags, "__dict__"):
            result = {}
            for key in ["generic", "rag"]:
                value = getattr(tags, key, None)
                if value is not None and not isinstance(value, Unset):
                    # Convert list of tag objects to list of dicts
                    if isinstance(value, list):
                        result[key] = [
                            item.to_dict()
                            if hasattr(item, "to_dict")
                            else dict(item)
                            if hasattr(item, "__dict__")
                            else item
                            for item in value
                        ]
                    else:
                        result[key] = value
            return result if result else None

        return None

    @property
    def rank(self) -> int | None:
        """
        Get the rank of this experiment compared to others in the project.

        Lower rank number means better performance. Rank 1 is the best-performing experiment.
        Ranking is calculated based on aggregate metrics and quality scores.

        Returns
        -------
            int | None: Rank number (1 = best), or None if not available.

        Examples
        --------
            experiments = Experiment.list(project_name="My Project")
            for exp in sorted(experiments, key=lambda x: x.rank or float('inf')):
                print(f"#{exp.rank}: {exp.name}")
        """
        if self._experiment_response is None:
            return None

        rank = getattr(self._experiment_response, "rank", None)
        if rank and not isinstance(rank, Unset):
            return int(rank)
        return None

    @property
    def ranking_score(self) -> float | None:
        """
        Get the ranking score for this experiment.

        This score is used to compare experiments. Higher scores indicate better performance.
        The score is calculated based on a combination of quality metrics and efficiency metrics.

        Returns
        -------
            float | None: Ranking score (higher is better), or None if not available.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My Project")
            experiment.refresh()

            if experiment.ranking_score:
                print(f"Ranking score: {experiment.ranking_score:.3f}")
        """
        if self._experiment_response is None:
            return None

        score = getattr(self._experiment_response, "ranking_score", None)
        if score and not isinstance(score, Unset):
            return float(score)
        return None

    @property
    def is_winner(self) -> bool:
        """
        Check if this experiment is marked as the winner.

        The winner is the best-performing experiment in a set of comparisons,
        typically the one with rank=1 and the highest ranking score.

        Returns
        -------
            bool: True if this experiment is the winner, False otherwise.

        Examples
        --------
            experiments = Experiment.list(project_name="My Project")
            winner = next((exp for exp in experiments if exp.is_winner), None)

            if winner:
                print(f"Best experiment: {winner.name}")
                print(f"Score: {winner.ranking_score}")
        """
        if self._experiment_response is None:
            return False

        winner = getattr(self._experiment_response, "winner", None)
        if winner and not isinstance(winner, Unset):
            return bool(winner)
        return False

    @property
    def model(self) -> Model | None:
        """
        Get the Model object for this experiment.

        Returns the Model if it was set during initialization, otherwise attempts
        to create a basic Model representation from the model_alias.

        Returns
        -------
            Model | None: Model object if available, None otherwise.

        Examples
        --------
            experiment = Experiment(
                name="ml-evaluation",
                dataset_name="ml-dataset",
                prompt_name="ml-prompt",
                model="gpt-4o-mini",
                project_name="My Project"
            )
            print(f"Model: {experiment.model.alias}")
        """
        if self._model_obj:
            return self._model_obj

        if self.model_alias:
            # Local import to avoid circular dependency
            from galileo.__future__.model import Model

            # Create a basic Model representation from the alias
            # Note: provider_name is unknown since we don't have integration context
            return Model(name=self.model_alias, alias=self.model_alias, provider_name="unknown")

        return None

    @property
    def prompt_model(self) -> str | None:
        """
        Get the model used in the prompt for this experiment.

        This is the model alias that was configured in the prompt settings
        when the experiment was run (e.g., "Claude 3.5 Haiku", "GPT-4o").

        Returns
        -------
            str | None: Model name, or None if not available.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My Project")
            print(f"Model used: {experiment.prompt_model}")
        """
        if self._experiment_response is None:
            return None

        model = getattr(self._experiment_response, "prompt_model", None)
        if model and not isinstance(model, Unset):
            return str(model)
        return None

    def add_tag(self, key: str, value: str, tag_type: str = "generic") -> None:
        """
        Add a tag to this experiment.

        Tags can be used to categorize, filter, and organize experiments.
        Common use cases include environment labels, version tracking, and team ownership.

        Args:
            key (str): Tag key (e.g., "environment", "version", "team")
            value (str): Tag value (e.g., "production", "1.0.0", "ml-team")
            tag_type (str): Tag category, defaults to "generic". Other options: "rag"

        Raises
        ------
            ValueError: If experiment hasn't been created yet (no id or project_id)

        Examples
        --------
            experiment = Experiment(
                name="ml-evaluation",
                dataset_name="ml-dataset",
                project_name="My Project"
            ).create()

            # Add multiple tags
            experiment.add_tag("environment", "production")
            experiment.add_tag("version", "1.0.0")
            experiment.add_tag("team", "ml-research")

            # View tags
            print(experiment.tags)
        """
        if self.id is None or self.project_id is None:
            raise ValueError("Experiment must be created before adding tags. Call .create() first.")

        try:
            _logger.info(f"Experiment.add_tag: id='{self.id}' {key}={value} type={tag_type} - started")
            upsert_experiment_tag(self.project_id, self.id, key, value, tag_type)
            _logger.info(f"Experiment.add_tag: id='{self.id}' - completed")

            # Refresh to get updated tags in the response
            self.refresh()
        except Exception as e:
            _logger.error(f"Experiment.add_tag: id='{self.id}' - failed: {e}")
            raise

    @property
    def span_columns(self) -> ColumnCollection:
        """
        Get available columns for spans in this experiment.

        Returns
        -------
            ColumnCollection: A collection of columns available for spans, accessible by column ID.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")
            columns = experiment.span_columns
            input_column = columns["input"]
        """
        response = self._get_columns(
            spans_available_columns_projects_project_id_spans_available_columns_post, "Unable to retrieve span columns"
        )
        columns = [Column(col) for col in response.columns]
        return ColumnCollection(columns)

    @property
    def session_columns(self) -> ColumnCollection:
        """
        Get available columns for sessions in this experiment.

        Returns
        -------
            ColumnCollection: A collection of columns available for sessions, accessible by column ID.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")
            columns = experiment.session_columns
            model_column = columns["model"]
        """
        response = self._get_columns(
            sessions_available_columns_projects_project_id_sessions_available_columns_post,
            "Unable to retrieve session columns",
        )
        columns = [Column(col) for col in response.columns]
        return ColumnCollection(columns)

    @property
    def trace_columns(self) -> ColumnCollection:
        """
        Get available columns for traces in this experiment.

        Returns
        -------
            ColumnCollection: A collection of columns available for traces, accessible by column ID.

        Examples
        --------
            experiment = Experiment.get(name="ml-evaluation", project_name="My AI Project")
            columns = experiment.trace_columns
            input_column = columns["input"]
        """
        response = self._get_columns(
            traces_available_columns_projects_project_id_traces_available_columns_post,
            "Unable to retrieve trace columns",
        )
        columns = [Column(col) for col in response.columns]
        return ColumnCollection(columns)


# Import at end to avoid circular import (dataset.py, prompt.py, project.py import Experiment)
from galileo.__future__.dataset import Dataset  # noqa: E402
from galileo.__future__.model import Model  # noqa: E402
from galileo.__future__.project import Project  # noqa: E402
from galileo.__future__.prompt import Prompt  # noqa: E402
from galileo.__future__.shared.column import Column, ColumnCollection  # noqa: E402
