from unittest.mock import Mock, patch
from uuid import uuid4

from galileo.resources.models import RunScorerSettingsResponse, ScorerConfig
from galileo.runs import update_scorer_settings

FIXED_PROJECT_ID = uuid4()
FIXED_RUN_ID = uuid4()


class TestUpdateScorerSettings:
    @patch("galileo.runs.upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_patch.sync")
    def test_successful_call(self, mock_api_call):
        mock_response = Mock(spec=RunScorerSettingsResponse)
        mock_api_call.return_value = mock_response
        mock_scorers = [Mock(spec=ScorerConfig)]

        response = update_scorer_settings(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID, scorers=mock_scorers)

        mock_api_call.assert_called_once()
        called_kwargs = mock_api_call.call_args[1]
        body = called_kwargs["body"]

        assert called_kwargs["project_id"] == str(FIXED_PROJECT_ID)
        assert called_kwargs["run_id"] == str(FIXED_RUN_ID)
        assert body.scorers == mock_scorers
        assert response == mock_response

    @patch("galileo.runs.upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_patch.sync")
    def test_api_failure_returns_none(self, mock_api_call):
        mock_api_call.return_value = None  # Simulate API failure
        mock_scorers = [Mock(spec=ScorerConfig)]

        response = update_scorer_settings(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID, scorers=mock_scorers)

        mock_api_call.assert_called_once()
        assert response is None
