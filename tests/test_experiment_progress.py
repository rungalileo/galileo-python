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
    @patch("time.sleep", return_value=None)
    def test_completes_when_status_reaches_100(self, mock_sleep, mock_get_status):
        mock_get_status.side_effect = [
            _make_status(0.0),
            _make_status(50.0),
            _make_status(100.0),
        ]
        exp = _make_experiment()
        exp.monitor_progress(poll_interval=0.0)
        assert mock_get_status.call_count == 3

    @patch("galileo.experiment.Experiment.get_status")
    @patch("time.sleep", return_value=None)
    def test_already_complete_on_first_poll(self, mock_sleep, mock_get_status):
        mock_get_status.return_value = _make_status(100.0)
        exp = _make_experiment()
        exp.monitor_progress(poll_interval=0.0)
        assert mock_get_status.call_count == 1
        mock_sleep.assert_not_called()

    @patch("galileo.experiment.Experiment.get_status")
    @patch("time.sleep", return_value=None)
    def test_uses_poll_interval(self, mock_sleep, mock_get_status):
        mock_get_status.side_effect = [_make_status(0.0), _make_status(100.0)]
        exp = _make_experiment()
        exp.monitor_progress(poll_interval=5.0)
        mock_sleep.assert_called_once_with(5.0)

    def test_raises_without_experiment_id(self):
        exp = Experiment._create_empty()
        exp.id = None
        exp.project_id = FIXED_PROJECT_ID
        with pytest.raises(ValueError, match="Experiment ID is not set"):
            exp.monitor_progress()

    def test_raises_without_project_id(self):
        exp = Experiment._create_empty()
        exp.id = FIXED_EXPERIMENT_ID
        exp.project_id = None
        with pytest.raises(ValueError, match="Project ID is not set"):
            exp.monitor_progress()
