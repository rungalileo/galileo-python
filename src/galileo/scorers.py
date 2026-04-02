import builtins
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
    ScorerIDFilter,
    ScorerIDFilterOperator,
    ScorerLabelFilter,
    ScorerLabelFilterOperator,
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

    def _list_with_filters(self, filters: list) -> list[ScorerResponse]:
        """Paginate through scorers/list with the given filters."""
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

    def list(self, name: Optional[str] = None, types: Optional[list[ScorerTypes]] = None) -> list[ScorerResponse]:
        """
        Lists scorers, optionally filtering by name and/or type.

        The filters are combined with an AND condition, while the values within the `types`
        list are combined with an OR condition.

        For example, calling `list(name="my_scorer", types=[ScorerTypes.llm, ScorerTypes.code])`
        will return scorers where the name is "my_scorer" AND the type is either "llm" OR "code".

        Parameters
        ----------
        name
            Name of the scorer to filter by.
        types
            List of scorer types to filter by. Defaults to all scorers.

        Returns
        -------
        A list of scorers that match the filter criteria.
        """
        filters = []
        if types:
            if len(types) == 1:
                filters.append(ScorerTypeFilter(value=types[0], operator=ScorerTypeFilterOperator.EQ))
            else:
                filters.append(ScorerTypeFilter(value=types, operator=ScorerTypeFilterOperator.ONE_OF))

        if name:
            filters.append(ScorerNameFilter(value=name, operator=ScorerNameFilterOperator.EQ))

        return self._list_with_filters(filters)

    def list_by_labels(self, labels: builtins.list[str], strict: bool = False) -> builtins.list[ScorerResponse]:
        """List scorers by label.

        Parameters
        ----------
        labels
            Label values to search for.
        strict
            When False (default), also matches by scorer name as a fallback
            for custom scorers that have no label set.

        Returns
        -------
        A list of scorers matching the label (or name) criteria.
        """
        if len(labels) == 1:
            label_filter = ScorerLabelFilter(
                value=labels[0], operator=ScorerLabelFilterOperator.EQ, case_sensitive=False, strict=strict
            )
        else:
            label_filter = ScorerLabelFilter(
                value=labels, operator=ScorerLabelFilterOperator.ONE_OF, case_sensitive=False, strict=strict
            )
        return self._list_with_filters([label_filter])

    def list_by_ids(self, scorer_ids: builtins.list[str]) -> builtins.list[ScorerResponse]:
        """List scorers by their UUIDs.

        Parameters
        ----------
        scorer_ids
            UUID strings of scorers to retrieve.

        Returns
        -------
        A list of scorers matching the given IDs.
        """
        if len(scorer_ids) == 1:
            id_filter = ScorerIDFilter(value=scorer_ids[0], operator=ScorerIDFilterOperator.EQ)
        else:
            id_filter = ScorerIDFilter(value=scorer_ids, operator=ScorerIDFilterOperator.ONE_OF)
        return self._list_with_filters([id_filter])

    def get_scorer_version(self, scorer_id: UUID, version: int) -> Union[Unset, BaseScorerVersionResponse]:
        """
        Parameters
        ----------
        name: str
            Name of the scorer
        version: int
            Version of the scorer.

        Returns
        -------
        Scorer response if found, otherwise None.
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
        Parameters
        ----------
        project_id
            ID of the project
        run_id
            ID of the run
        scorers
            List of scorer configurations

        Returns
        -------
        Upserted scorer settings.
        """
        return upsert_scorers_config_projects_project_id_runs_run_id_scorer_settings_post.sync(
            project_id=project_id,
            run_id=run_id,
            client=self.config.api_client,
            body=RunScorerSettingsPatchRequest(run_id=run_id, scorers=scorers),
        )
