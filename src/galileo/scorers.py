from galileo.base import BaseClientModel
from galileo.resources.api.data import list_scorers_with_filters_scorers_list_post
from galileo.resources.api.run_scorer_settings import (
    upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_post,
)
from galileo.resources.models import (
    ListScorersRequest,
    RunScorerSettingsRequest,
    ScorerConfig,
    ScorerTypeFilter,
    ScorerTypeFilterOperator,
    ScorerTypes,
)


class Scorers(BaseClientModel):
    def list(self, types: list[ScorerTypes] = None):
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


class ScorerSettings(BaseClientModel):
    def create(self, project_id: str, run_id: str, scorers: list[ScorerConfig]):
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
            body=RunScorerSettingsRequest(run_id=run_id, scorers=scorers),
        )
