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
from galileo.utils.catch_log import DecorateAllMethods

logger = logging.getLogger(__name__)


class Runs(BaseClientModel, DecorateAllMethods):
    def update_scorer_settings(
        self,
        project_id: UUID4,
        run_id: UUID4,
        scorers: list[ScorerConfig],
        segment_filters: Optional[list[SegmentFilter]] = None,
    ) -> Optional[RunScorerSettingsResponse]:
        """
        Updates the scorer settings for a specific run.
        """
        body = RunScorerSettingsPatchRequest(run_id=str(run_id), scorers=scorers, segment_filters=segment_filters)

        response = upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_patch.sync(
            client=self.client, project_id=str(project_id), run_id=str(run_id), body=body
        )
        logger.debug(f"Update scorer settings response: {response}")

        if not isinstance(response, RunScorerSettingsResponse):
            if isinstance(response, HTTPValidationError):
                logger.error(f"Validation error updating scorer settings: {response}")
            else:
                logger.error(f"Failed to update scorer settings. Response: {response}")
            return None

        return response


def update_scorer_settings(
    project_id: UUID4, run_id: UUID4, scorers: list[ScorerConfig], segment_filters: Optional[list[SegmentFilter]] = None
) -> Optional[RunScorerSettingsResponse]:
    """
    A helper function to update the scorer settings for a specific run.
    """
    runs_client = Runs()
    return runs_client.update_scorer_settings(
        project_id=project_id, run_id=run_id, scorers=scorers, segment_filters=segment_filters
    )
