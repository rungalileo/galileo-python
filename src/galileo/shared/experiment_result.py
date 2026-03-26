"""Experiment result wrapper for easy status access and monitoring."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from galileo.resources.types import Unset

if TYPE_CHECKING:
    from galileo.resources.models import ExperimentResponse

logger = logging.getLogger(__name__)


class ExperimentPhaseInfo:
    """
    Wrapper for experiment phase status information.

    Provides easy access to phase-level progress and status information for an experiment.

    Attributes
    ----------
        progress_percent (float): Progress percentage (0.0 to 100.0).
        is_complete (bool): Whether this phase is complete.
        is_failed (bool): Whether this phase failed.
        is_in_progress (bool): Whether this phase is in progress.

    Examples
    --------
        # Access phase information from experiment status
        experiment = Experiment.get(name="ml-eval", project_name="My Project")
        status = experiment.get_status()

        log_gen = status.log_generation
        if log_gen.is_complete:
            print("Log generation phase completed!")
        elif log_gen.is_in_progress:
            print(f"Log generation at {log_gen.progress_percent:.1f}%")

        # Check phase status
        print(f"Phase status: {log_gen}")  # Human-readable string
    """

    def __init__(self, phase_status: Any):
        """
        Initialize from ExperimentPhaseStatus object.

        Args:
            phase_status: The phase status object from the API response.
        """
        self.progress_percent = getattr(phase_status, "progress_percent", 0.0)
        if isinstance(self.progress_percent, Unset):
            self.progress_percent = 0.0
        # Convert from API's 0.0-1.0 range to 0.0-100.0 percentage
        self.progress_percent = self.progress_percent * 100.0

    @property
    def is_complete(self) -> bool:
        """Whether this phase is complete (progress >= 100%)."""
        return self.progress_percent >= 100.0

    @property
    def is_failed(self) -> bool:
        """Whether this phase failed. Currently always returns False."""
        # TODO: Check for actual failure status when available in API
        return False

    @property
    def is_in_progress(self) -> bool:
        """Whether this phase is in progress (0% < progress < 100%)."""
        return 0.0 < self.progress_percent < 100.0

    @property
    def is_pending(self) -> bool:
        """Whether this phase hasn't started yet (progress = 0%)."""
        return self.progress_percent == 0.0

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the phase info to a dictionary.

        Returns
        -------
            A dictionary containing phase status information.

        Examples
        --------
            phase_dict = status.log_generation.to_dict()
            print(phase_dict["progress_percent"])
            print(phase_dict["is_complete"])
        """
        return {
            "progress_percent": self.progress_percent,
            "is_complete": self.is_complete,
            "is_failed": self.is_failed,
            "is_in_progress": self.is_in_progress,
            "is_pending": self.is_pending,
        }

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"ExperimentPhaseInfo(progress_percent={self.progress_percent:.1f}, "
            f"is_complete={self.is_complete}, is_in_progress={self.is_in_progress})"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        if self.is_complete:
            return "Complete (100%)"
        if self.is_in_progress:
            return f"In Progress ({self.progress_percent:.1f}%)"
        return "Not Started (0%)"


class ExperimentStatusInfo:
    """
    Wrapper for experiment status information.

    Provides human-readable access to experiment execution status, including progress
    tracking and phase-level information.

    Attributes
    ----------
        log_generation (ExperimentPhaseInfo): Status of log generation phase.
        overall_progress (float): Overall progress percentage (0.0 to 100.0).
        is_complete (bool): Whether the experiment is complete.
        is_in_progress (bool): Whether the experiment is currently running.
        is_pending (bool): Whether the experiment hasn't started yet.

    Examples
    --------
        # Get status information
        experiment = Experiment.get(name="ml-eval", project_name="My Project")
        status = experiment.get_status()

        # Human-readable output
        print(status)  # "Experiment Running (45.2%)"
        print(f"Log Generation: {status.log_generation}")  # "In Progress (45.2%)"

        # Check status
        if status.is_complete:
            print("Experiment completed!")
        elif status.is_in_progress:
            print(f"Progress: {status.overall_progress:.1f}%")
        elif status.is_pending:
            print("Experiment hasn't started yet")

        # Convert to dictionary
        status_dict = status.to_dict()
        print(status_dict["overall_progress"])
    """

    def __init__(self, experiment_response: ExperimentResponse):
        """
        Initialize from ExperimentResponse object.

        Args:
            experiment_response: The experiment response from the API.
        """
        self._response = experiment_response

        # Extract status info with proper handling of Unset types
        status_obj = getattr(experiment_response, "status", None)
        if status_obj is not None and not isinstance(status_obj, Unset):
            log_gen = getattr(status_obj, "log_generation", None)
            if log_gen is not None and not isinstance(log_gen, Unset):
                self.log_generation = ExperimentPhaseInfo(log_gen)
            else:
                self.log_generation = ExperimentPhaseInfo(type("obj", (), {"progress_percent": 0.0})())
        else:
            self.log_generation = ExperimentPhaseInfo(type("obj", (), {"progress_percent": 0.0})())

    @classmethod
    def from_result(cls, result: dict[str, Any]) -> ExperimentStatusInfo:
        """
        Create from experiment.run() result dictionary.

        Args:
            result: Dictionary returned from Experiment.run().

        Returns
        -------
            ExperimentStatusInfo: Status information extracted from the result.

        Examples
        --------
            result = experiment.run()
            status = ExperimentStatusInfo.from_result(result)
            print(f"Status: {status}")
        """
        return cls(result["experiment"])

    @property
    def overall_progress(self) -> float:
        """
        Overall progress percentage across all phases.

        Currently uses log_generation progress. In the future, this may
        average multiple phase progress values.

        Returns
        -------
            float: Progress percentage from 0.0 to 100.0.
        """
        # For now just use log_generation progress
        # Could average multiple phases in the future
        return self.log_generation.progress_percent

    @property
    def is_complete(self) -> bool:
        """Whether the experiment is complete (all phases at 100%)."""
        return self.log_generation.is_complete

    @property
    def is_in_progress(self) -> bool:
        """Whether the experiment is currently running (0% < progress < 100%)."""
        return self.log_generation.is_in_progress

    @property
    def is_pending(self) -> bool:
        """Whether the experiment hasn't started yet (progress = 0%)."""
        return self.overall_progress == 0.0

    @property
    def is_failed(self) -> bool:
        """Whether the experiment has failed. Currently always returns False."""
        # TODO: Check for actual failure status when available in API
        return self.log_generation.is_failed

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the status info to a dictionary.

        Returns
        -------
            A dictionary containing status information.

        Examples
        --------
            status = experiment.get_status()
            status_dict = status.to_dict()
            print(status_dict["overall_progress"])
            print(status_dict["log_generation"]["is_complete"])
        """
        return {
            "overall_progress": self.overall_progress,
            "is_complete": self.is_complete,
            "is_in_progress": self.is_in_progress,
            "is_pending": self.is_pending,
            "is_failed": self.is_failed,
            "log_generation": self.log_generation.to_dict(),
        }

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"ExperimentStatusInfo(\n"
            f"  log_generation={self.log_generation!r},\n"
            f"  overall_progress={self.overall_progress:.1f}%,\n"
            f"  is_complete={self.is_complete},\n"
            f"  is_in_progress={self.is_in_progress}\n"
            f")"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        if self.is_complete:
            return "Experiment Complete"
        if self.is_in_progress:
            return f"Experiment Running ({self.overall_progress:.1f}%)"
        return "Experiment Pending"


class ExperimentRunResult:
    """
    Wrapper for experiment.run() result with human-readable access.

    Provides easy access to experiment run information including the link,
    status, and underlying experiment response. This wrapper makes it simple
    to work with experiment run results by exposing commonly needed information
    through intuitive properties and methods.

    Attributes
    ----------
        link (str): URL to view experiment results in Galileo console.
        message (str): Status message about the experiment.
        status (ExperimentStatusInfo): Detailed status information.
        experiment_id (str): The experiment ID.
        project_id (str): The project ID.
        experiment_name (str): The experiment name.

    Examples
    --------
        # Run an experiment and access the result
        experiment = Experiment(
            name="ml-evaluation",
            dataset_name="ml-dataset",
            prompt_name="ml-prompt",
            project_name="My AI Project"
        ).create()

        result = experiment.run()

        # Access basic information
        print(result)  # Human-readable summary
        print(f"View results: {result.link}")
        print(f"Experiment ID: {result.experiment_id}")

        # Check status
        if result.status.is_in_progress:
            print(f"Progress: {result.status.overall_progress:.1f}%")
        elif result.status.is_complete:
            print("Experiment completed!")

        # Get dataset and prompt information
        if result.dataset_info:
            print(f"Dataset: {result.dataset_info['name']}")
        if result.prompt_info:
            print(f"Prompt: {result.prompt_info['name']}")

        # Convert to dictionary
        result_dict = result.to_dict()
        print(result_dict["link"])
    """

    def __init__(self, result: dict[str, Any]):
        """
        Initialize from experiment.run() result.

        Args:
            result: Dictionary returned from Experiment.run().

        Raises
        ------
            KeyError: If required keys are missing from result dictionary.
            TypeError: If result is not a dictionary.
        """
        if not isinstance(result, dict):
            raise TypeError(f"Expected dict, got {type(result).__name__}")

        if "experiment" not in result:
            raise KeyError("Result dictionary missing required key 'experiment'")

        self._result = result
        self._experiment_response: ExperimentResponse = result["experiment"]
        self.link = result.get("link", "")
        self.message = result.get("message", "")
        self.status = ExperimentStatusInfo(self._experiment_response)
        self.experiment_id = self._experiment_response.id
        self.project_id = self._experiment_response.project_id
        self.experiment_name = getattr(self._experiment_response, "name", "")

    @property
    def experiment(self) -> ExperimentResponse:
        """
        Get the underlying ExperimentResponse object.

        Returns
        -------
            ExperimentResponse: The raw API response object.
        """
        return self._experiment_response

    @property
    def dataset_info(self) -> dict[str, str | None] | None:
        """
        Get dataset information if available.

        Returns
        -------
            dict or None: Dictionary with dataset id, name, and version, or None if no dataset.

        Examples
        --------
            result = experiment.run()
            if result.dataset_info:
                print(f"Dataset: {result.dataset_info['name']}")
                print(f"Version: {result.dataset_info['version']}")
        """
        dataset = getattr(self._experiment_response, "dataset", None)
        if dataset is None or isinstance(dataset, Unset):
            return None

        return {
            "id": getattr(dataset, "dataset_id", None),
            "name": getattr(dataset, "name", None),
            "version": getattr(dataset, "version_index", None),
        }

    @property
    def prompt_info(self) -> dict[str, str | None] | None:
        """
        Get prompt information if available.

        Returns
        -------
            dict or None: Dictionary with prompt id and name, or None if no prompt.

        Examples
        --------
            result = experiment.run()
            if result.prompt_info:
                print(f"Prompt: {result.prompt_info['name']}")
                print(f"ID: {result.prompt_info['id']}")
        """
        prompt = getattr(self._experiment_response, "prompt", None)
        if prompt is None or isinstance(prompt, Unset):
            return None

        return {"id": getattr(prompt, "prompt_template_id", None), "name": getattr(prompt, "name", None)}

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the result to a dictionary.

        Returns
        -------
            A dictionary containing all result information.

        Examples
        --------
            result = experiment.run()
            result_dict = result.to_dict()
            print(result_dict["link"])
            print(result_dict["status"]["overall_progress"])
        """
        return {
            "experiment_id": self.experiment_id,
            "experiment_name": self.experiment_name,
            "project_id": self.project_id,
            "link": self.link,
            "message": self.message,
            "status": self.status.to_dict(),
            "dataset_info": self.dataset_info,
            "prompt_info": self.prompt_info,
        }

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"ExperimentRunResult(\n"
            f"  experiment_id='{self.experiment_id}',\n"
            f"  experiment_name='{self.experiment_name}',\n"
            f"  project_id='{self.project_id}',\n"
            f"  status={self.status!r},\n"
            f"  link='{self.link}',\n"
            f"  dataset_info={self.dataset_info},\n"
            f"  prompt_info={self.prompt_info}\n"
            f")"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        lines = [
            "=" * 70,
            f"Experiment: {self.experiment_name}",
            "=" * 70,
            f"Status: {self.status}",
            f"Link: {self.link}",
            "",
        ]

        if self.dataset_info:
            dataset_name = self.dataset_info.get("name", "N/A")
            dataset_id = self.dataset_info.get("id", "N/A")
            lines.append(f"Dataset: {dataset_name} (id: {dataset_id})")

        if self.prompt_info:
            prompt_name = self.prompt_info.get("name", "N/A")
            prompt_id = self.prompt_info.get("id", "N/A")
            lines.append(f"Prompt: {prompt_name} (id: {prompt_id})")

        lines.append("=" * 70)

        return "\n".join(lines)
