import logging
from typing import Optional

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.resources.api.run_scorer_settings import (
    upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_patch,
)
from galileo.resources.models import (
    HTTPValidationError,
    RunScorerSettingsPatchRequest,
    RunScorerSettingsResponse,
    ScorerConfig,
    SegmentFilter,
)

logger = logging.getLogger(__name__)


class Runs(BaseClientModel):
    def update_scorer_settings(
        self,
        project_id: UUID4,
        run_id: UUID4,
        scorers: list[ScorerConfig],
        segment_filters: Optional[list[SegmentFilter]] = None,
    ) -> RunScorerSettingsResponse:
        body = RunScorerSettingsPatchRequest(run_id=str(run_id), scorers=scorers, segment_filters=segment_filters)

        response = upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_patch.sync(
            client=self.client, project_id=str(project_id), run_id=str(run_id), body=body
        )

        if isinstance(response, HTTPValidationError):
            raise ValueError(response.detail)
        if not response:
            raise ValueError("Failed to update scorer settings")

        return response


def update_scorer_settings(
    project_id: UUID4, run_id: UUID4, scorers: list[ScorerConfig], segment_filters: Optional[list[SegmentFilter]] = None
) -> RunScorerSettingsResponse:
    """Updates the scorer settings for a specific run.

    Args:
        project_id: The unique identifier of the project.
        run_id: The unique identifier of the run.
        scorers: A list of scorer configurations to apply to the run.
        segment_filters: A list of segment filters to apply to the run.

    Returns:
        A RunScorerSettingsResponse object containing the updated settings.
    """
    return Runs().update_scorer_settings(
        project_id=project_id, run_id=run_id, scorers=scorers, segment_filters=segment_filters
    )
