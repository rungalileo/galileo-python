from galileo.base import BaseClientModel
from galileo.resources.api.data import list_scorers_with_filters_scorers_list_post
from galileo.resources.api.run_scorer_settings import (
    upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_post,
)
from galileo.resources.models import (
    ListScorersRequest,
    RunScorerSettingsRequest,
    ScorerTypeFilter,
    ScorerTypeFilterOperator,
    ScorerTypes,
)


class Scorers(BaseClientModel):
    def list(self):
        body = ListScorersRequest(
            filters=[ScorerTypeFilter(value=ScorerTypes.PRESET, operator=ScorerTypeFilterOperator.EQ)]
        )
        result = list_scorers_with_filters_scorers_list_post.sync(client=self.client, body=body)
        return result.scorers


class ScorerSettings(BaseClientModel):
    def create(self, project_id, run_id, scorers):
        return upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_post.sync(
            project_id=project_id,
            run_id=run_id,
            client=self.client,
            body=RunScorerSettingsRequest(run_id=run_id, scorers=scorers),
        )
