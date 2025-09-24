import re
from unittest.mock import Mock, patch
from uuid import uuid4

import pytest

from galileo.resources.models import HTTPValidationError, RunScorerSettingsResponse, ScorerConfig, ValidationError
from galileo.runs import update_scorer_settings

FIXED_PROJECT_ID = str(uuid4())
FIXED_RUN_ID = str(uuid4())


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

        assert called_kwargs["project_id"] == FIXED_PROJECT_ID
        assert called_kwargs["run_id"] == FIXED_RUN_ID
        assert body.scorers == mock_scorers
        assert response == mock_response

    @patch("galileo.runs.upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_patch.sync")
    def test_api_failure_raises_value_error(self, mock_api_call):
        mock_api_call.return_value = None
        mock_scorers = [Mock(spec=ScorerConfig)]

        with pytest.raises(ValueError, match="Failed to update scorer settings"):
            update_scorer_settings(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID, scorers=mock_scorers)

        mock_api_call.assert_called_once()

    @patch("galileo.runs.upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_patch.sync")
    def test_http_validation_error_raises_exception(self, mock_api_call):
        detail = [ValidationError(loc=["body", "project_id"], msg="value is not a valid uuid", type_="type_error.uuid")]
        mock_api_call.return_value = HTTPValidationError(detail=detail)
        mock_scorers = [Mock(spec=ScorerConfig)]

        with pytest.raises(ValueError, match=re.escape(str(detail))):
            update_scorer_settings(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID, scorers=mock_scorers)
