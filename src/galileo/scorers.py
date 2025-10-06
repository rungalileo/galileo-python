from typing import Optional, Union
from uuid import UUID

from galileo.config import GalileoPythonConfig
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
    ListScorersResponse,
    ScorerConfig,
    ScorerNameFilter,
    ScorerNameFilterOperator,
    ScorerResponse,
    ScorerTypeFilter,
    ScorerTypeFilterOperator,
    ScorerTypes,
)
from galileo.resources.models.base_scorer_version_response import BaseScorerVersionResponse
from galileo.resources.models.run_scorer_settings_patch_request import RunScorerSettingsPatchRequest
from galileo.resources.models.run_scorer_settings_response import RunScorerSettingsResponse
from galileo.resources.types import Unset


class Scorers:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def list(self, name: Optional[str] = None, types: Optional[list[ScorerTypes]] = None) -> list[ScorerResponse]:
        """
        Args:
            name: Name of the scorer to filter by.
            types: List of scorer types to filter by. Defaults to all scorers.
        Returns:
            List of scorers
        """
        filters = [ScorerTypeFilter(value=type_, operator=ScorerTypeFilterOperator.EQ) for type_ in (types or [])]
        if name:
            filters.append(ScorerNameFilter(value=name, operator=ScorerNameFilterOperator.EQ))

        body = ListScorersRequest(filters=filters)

        all_scorers: list[ScorerResponse] = []
        starting_token = 0
        while True:
            result = list_scorers_with_filters_scorers_list_post.sync(
                client=self.config.api_client, body=body, starting_token=starting_token
            )

            if not isinstance(result, ListScorersResponse):
                raise ValueError(f"Failed to list scorers, got response: {result}")

            if not isinstance(result.scorers, Unset):
                all_scorers.extend(result.scorers)

            if isinstance(result.next_starting_token, int):
                starting_token = result.next_starting_token
            else:
                break

        return all_scorers

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
        return get_scorer_version_or_latest_scorers_scorer_id_version_get.sync(
            scorer_id=scorer_id, version=version, client=self.config.api_client
        )


class ScorerSettings:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

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
            client=self.config.api_client,
            body=RunScorerSettingsPatchRequest(run_id=run_id, scorers=scorers),
        )
