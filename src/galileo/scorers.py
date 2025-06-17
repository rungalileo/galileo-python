from typing import Optional, Union
from uuid import UUID

from galileo.base import BaseClientModel
from galileo.resources.api.data import (
    get_scorer_version_or_latest_scorers_scorer_id_version_get,
    list_scorers_with_filters_scorers_list_post,
)
from galileo.resources.api.run_scorer_settings import (
    upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_post,
)
from galileo.resources.models import (
    HTTPValidationError,
    ListScorersRequest,
    ScorerConfig,
    ScorerResponse,
    ScorerTypeFilter,
    ScorerTypeFilterOperator,
    ScorerTypes,
)
from galileo.resources.models.base_scorer_version_response import BaseScorerVersionResponse
from galileo.resources.models.run_scorer_settings_patch_request import RunScorerSettingsPatchRequest
from galileo.resources.models.run_scorer_settings_response import RunScorerSettingsResponse
from galileo.resources.types import Unset


class Scorers(BaseClientModel):
    def list(self, types: list[ScorerTypes] = None) -> Union[Unset, list[ScorerResponse]]:
        """
        Args:
            types: List of scorer types to filter by. Defaults to all scorers.
        Returns:
            List of scorers
        """
        body = ListScorersRequest(
            filters=[ScorerTypeFilter(value=type_, operator=ScorerTypeFilterOperator.EQ) for type_ in (types or [])]
        )
        result = list_scorers_with_filters_scorers_list_post.sync(client=self.client, body=body)
        return result.scorers

    def get_scorer_version(self, scorer_id: UUID, version: int) -> Union[Unset, BaseScorerVersionResponse]:
        """
        Args:
            name: str
                Name of the scorer
            version: int
                Version of the scorer.
        Returns:
            Scorer response if found, otherwise None
        """
        result = get_scorer_version_or_latest_scorers_scorer_id_version_get.sync(
            scorer_id=scorer_id, version=version, client=self.client
        )
        return result


class ScorerSettings(BaseClientModel):
    def create(
        self, project_id: str, run_id: str, scorers: list[ScorerConfig]
    ) -> Optional[Union[HTTPValidationError, RunScorerSettingsResponse]]:
        """
        Args:
            project_id: ID of the project
            run_id: ID of the run
            scorers: List of scorer configurations
        Returns:
            Upserted scorer settings
        """
        return upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_post.sync(
            project_id=project_id,
            run_id=run_id,
            client=self.client,
            body=RunScorerSettingsPatchRequest(run_id=run_id, scorers=scorers),
        )
