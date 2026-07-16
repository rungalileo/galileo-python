from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.experiment import Experiment
from galileo.shared.base import SyncState
from galileo.shared.experiment_result import ExperimentStatusInfo

FIXED_PROJECT_ID = str(uuid4())
FIXED_EXPERIMENT_ID = str(uuid4())


def _make_status(progress_percent: float) -> ExperimentStatusInfo:
    """Build an ExperimentStatusInfo with a given log_generation progress (0-100)."""
    phase = MagicMock()
    phase.progress_percent = progress_percent / 100.0  # API uses 0.0-1.0
    response = MagicMock()
    response.status.log_generation = phase
    return ExperimentStatusInfo(response)


def _make_experiment() -> Experiment:
    exp = Experiment._create_empty()
    exp.id = FIXED_EXPERIMENT_ID
    exp.project_id = FIXED_PROJECT_ID
    exp.name = "test-experiment"
    exp._set_state(SyncState.SYNCED)
    return exp


class TestMonitorProgress:
    @patch("galileo.experiment.Experiment.get_status")
    @patch("galileo.experiment.sleep", return_value=None)
    def test_completes_when_status_reaches_100(self, mock_sleep, mock_get_status):
        # Given: an experiment that progresses through 0%, 50%, then 100%
        mock_get_status.side_effect = [_make_status(0.0), _make_status(50.0), _make_status(100.0)]
        exp = _make_experiment()

        # When: monitoring progress until completion
        exp.monitor_progress(poll_interval_seconds=0.0)

        # Then: get_status is polled until 100% is reached
        assert mock_get_status.call_count == 3

    @patch("galileo.experiment.Experiment.get_status")
    @patch("galileo.experiment.sleep", return_value=None)
    def test_already_complete_on_first_poll(self, mock_sleep, mock_get_status):
        # Given: an experiment that is already at 100% on the first poll
        mock_get_status.return_value = _make_status(100.0)
        exp = _make_experiment()

        # When: monitoring progress
        exp.monitor_progress(poll_interval_seconds=0.0)

        # Then: get_status is called once and sleep is never called
        assert mock_get_status.call_count == 1
        mock_sleep.assert_not_called()

    @patch("galileo.experiment.Experiment.get_status")
    @patch("galileo.experiment.sleep", return_value=None)
    def test_uses_poll_interval_seconds(self, mock_sleep, mock_get_status):
        # Given: an experiment that completes on the second poll
        mock_get_status.side_effect = [_make_status(0.0), _make_status(100.0)]
        exp = _make_experiment()

        # When: monitoring with a custom poll interval
        exp.monitor_progress(poll_interval_seconds=5.0)

        # Then: sleep is called once with the specified interval
        mock_sleep.assert_called_once_with(5.0)

    def test_raises_without_experiment_id(self):
        # Given: an experiment without an id
        exp = Experiment._create_empty()
        exp.id = None
        exp.project_id = FIXED_PROJECT_ID

        # When/Then: monitoring raises ValueError about the missing experiment id
        with pytest.raises(ValueError, match="Experiment ID is not set"):
            exp.monitor_progress()

    def test_raises_without_project_id(self):
        # Given: an experiment without a project_id
        exp = Experiment._create_empty()
        exp.id = FIXED_EXPERIMENT_ID
        exp.project_id = None

        # When/Then: monitoring raises ValueError about the missing project id
        with pytest.raises(ValueError, match="Project ID is not set"):
            exp.monitor_progress()

    @patch("galileo.experiment.Experiment.get_status")
    @patch("galileo.experiment.sleep", return_value=None)
    def test_deprecated_job_id_warns(self, mock_sleep, mock_get_status):
        # Given: an experiment that is already complete, and a caller passing the deprecated job_id
        mock_get_status.return_value = _make_status(100.0)
        exp = _make_experiment()

        # When/Then: monitor_progress emits a DeprecationWarning when job_id is supplied
        with pytest.warns(DeprecationWarning, match="job_id"):
            exp.monitor_progress(job_id="some-old-job-id")
