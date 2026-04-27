from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.task_type import TaskType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_dataset import ExperimentDataset
    from ..models.experiment_playground import ExperimentPlayground
    from ..models.experiment_prompt import ExperimentPrompt
    from ..models.experiment_response_aggregate_feedback import ExperimentResponseAggregateFeedback
    from ..models.experiment_response_aggregate_metrics import ExperimentResponseAggregateMetrics
    from ..models.experiment_response_rating_aggregates import ExperimentResponseRatingAggregates
    from ..models.experiment_response_structured_aggregate_metrics_type_0 import (
        ExperimentResponseStructuredAggregateMetricsType0,
    )
    from ..models.experiment_response_tags import ExperimentResponseTags
    from ..models.experiment_status import ExperimentStatus
    from ..models.prompt_run_settings_output import PromptRunSettingsOutput
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="ExperimentResponse")


@_attrs_define
class ExperimentResponse:
    """
    Attributes:
        id (str): Galileo ID of the experiment
        project_id (str): Galileo ID of the project associated with this experiment
        task_type (TaskType): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the database frequently.
        created_at (datetime.datetime | Unset): Timestamp of the experiment's creation
        updated_at (datetime.datetime | None | Unset): Timestamp of the trace or span's last update
        name (str | Unset): Name of the experiment Default: ''.
        created_by (None | str | Unset):
        created_by_user (None | Unset | UserInfo):
        num_spans (int | None | Unset):
        num_traces (int | None | Unset):
        dataset (ExperimentDataset | None | Unset):
        aggregate_metrics (ExperimentResponseAggregateMetrics | Unset):
        structured_aggregate_metrics (ExperimentResponseStructuredAggregateMetricsType0 | None | Unset): Structured
            aggregate metrics keyed by raw metric name with full statistical aggregates. Present only when
            use_clickhouse_run_aggregates flag is enabled.
        aggregate_feedback (ExperimentResponseAggregateFeedback | Unset): Aggregate feedback information related to the
            experiment (traces only)
        rating_aggregates (ExperimentResponseRatingAggregates | Unset): Annotation aggregates keyed by template ID and
            root type
        ranking_score (float | None | Unset):
        rank (int | None | Unset):
        winner (bool | None | Unset):
        playground_id (None | str | Unset):
        playground (ExperimentPlayground | None | Unset):
        prompt_run_settings (None | PromptRunSettingsOutput | Unset):
        prompt_model (None | str | Unset):
        prompt (ExperimentPrompt | None | Unset):
        tags (ExperimentResponseTags | Unset):
        status (ExperimentStatus | Unset):
    """

    id: str
    project_id: str
    task_type: TaskType
    created_at: datetime.datetime | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    name: str | Unset = ""
    created_by: None | str | Unset = UNSET
    created_by_user: None | Unset | UserInfo = UNSET
    num_spans: int | None | Unset = UNSET
    num_traces: int | None | Unset = UNSET
    dataset: ExperimentDataset | None | Unset = UNSET
    aggregate_metrics: ExperimentResponseAggregateMetrics | Unset = UNSET
    structured_aggregate_metrics: ExperimentResponseStructuredAggregateMetricsType0 | None | Unset = UNSET
    aggregate_feedback: ExperimentResponseAggregateFeedback | Unset = UNSET
    rating_aggregates: ExperimentResponseRatingAggregates | Unset = UNSET
    ranking_score: float | None | Unset = UNSET
    rank: int | None | Unset = UNSET
    winner: bool | None | Unset = UNSET
    playground_id: None | str | Unset = UNSET
    playground: ExperimentPlayground | None | Unset = UNSET
    prompt_run_settings: None | PromptRunSettingsOutput | Unset = UNSET
    prompt_model: None | str | Unset = UNSET
    prompt: ExperimentPrompt | None | Unset = UNSET
    tags: ExperimentResponseTags | Unset = UNSET
    status: ExperimentStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.experiment_dataset import ExperimentDataset
        from ..models.experiment_playground import ExperimentPlayground
        from ..models.experiment_prompt import ExperimentPrompt
        from ..models.experiment_response_structured_aggregate_metrics_type_0 import (
            ExperimentResponseStructuredAggregateMetricsType0,
        )
        from ..models.prompt_run_settings_output import PromptRunSettingsOutput
        from ..models.user_info import UserInfo

        id = self.id

        project_id = self.project_id

        task_type = self.task_type.value

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        name = self.name

        created_by: None | str | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        created_by_user: dict[str, Any] | None | Unset
        if isinstance(self.created_by_user, Unset):
            created_by_user = UNSET
        elif isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        num_spans: int | None | Unset
        if isinstance(self.num_spans, Unset):
            num_spans = UNSET
        else:
            num_spans = self.num_spans

        num_traces: int | None | Unset
        if isinstance(self.num_traces, Unset):
            num_traces = UNSET
        else:
            num_traces = self.num_traces

        dataset: dict[str, Any] | None | Unset
        if isinstance(self.dataset, Unset):
            dataset = UNSET
        elif isinstance(self.dataset, ExperimentDataset):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        aggregate_metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.aggregate_metrics, Unset):
            aggregate_metrics = self.aggregate_metrics.to_dict()

        structured_aggregate_metrics: dict[str, Any] | None | Unset
        if isinstance(self.structured_aggregate_metrics, Unset):
            structured_aggregate_metrics = UNSET
        elif isinstance(self.structured_aggregate_metrics, ExperimentResponseStructuredAggregateMetricsType0):
            structured_aggregate_metrics = self.structured_aggregate_metrics.to_dict()
        else:
            structured_aggregate_metrics = self.structured_aggregate_metrics

        aggregate_feedback: dict[str, Any] | Unset = UNSET
        if not isinstance(self.aggregate_feedback, Unset):
            aggregate_feedback = self.aggregate_feedback.to_dict()

        rating_aggregates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rating_aggregates, Unset):
            rating_aggregates = self.rating_aggregates.to_dict()

        ranking_score: float | None | Unset
        if isinstance(self.ranking_score, Unset):
            ranking_score = UNSET
        else:
            ranking_score = self.ranking_score

        rank: int | None | Unset
        if isinstance(self.rank, Unset):
            rank = UNSET
        else:
            rank = self.rank

        winner: bool | None | Unset
        if isinstance(self.winner, Unset):
            winner = UNSET
        else:
            winner = self.winner

        playground_id: None | str | Unset
        if isinstance(self.playground_id, Unset):
            playground_id = UNSET
        else:
            playground_id = self.playground_id

        playground: dict[str, Any] | None | Unset
        if isinstance(self.playground, Unset):
            playground = UNSET
        elif isinstance(self.playground, ExperimentPlayground):
            playground = self.playground.to_dict()
        else:
            playground = self.playground

        prompt_run_settings: dict[str, Any] | None | Unset
        if isinstance(self.prompt_run_settings, Unset):
            prompt_run_settings = UNSET
        elif isinstance(self.prompt_run_settings, PromptRunSettingsOutput):
            prompt_run_settings = self.prompt_run_settings.to_dict()
        else:
            prompt_run_settings = self.prompt_run_settings

        prompt_model: None | str | Unset
        if isinstance(self.prompt_model, Unset):
            prompt_model = UNSET
        else:
            prompt_model = self.prompt_model

        prompt: dict[str, Any] | None | Unset
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        elif isinstance(self.prompt, ExperimentPrompt):
            prompt = self.prompt.to_dict()
        else:
            prompt = self.prompt

        tags: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        status: dict[str, Any] | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "project_id": project_id, "task_type": task_type})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if name is not UNSET:
            field_dict["name"] = name
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_by_user is not UNSET:
            field_dict["created_by_user"] = created_by_user
        if num_spans is not UNSET:
            field_dict["num_spans"] = num_spans
        if num_traces is not UNSET:
            field_dict["num_traces"] = num_traces
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if aggregate_metrics is not UNSET:
            field_dict["aggregate_metrics"] = aggregate_metrics
        if structured_aggregate_metrics is not UNSET:
            field_dict["structured_aggregate_metrics"] = structured_aggregate_metrics
        if aggregate_feedback is not UNSET:
            field_dict["aggregate_feedback"] = aggregate_feedback
        if rating_aggregates is not UNSET:
            field_dict["rating_aggregates"] = rating_aggregates
        if ranking_score is not UNSET:
            field_dict["ranking_score"] = ranking_score
        if rank is not UNSET:
            field_dict["rank"] = rank
        if winner is not UNSET:
            field_dict["winner"] = winner
        if playground_id is not UNSET:
            field_dict["playground_id"] = playground_id
        if playground is not UNSET:
            field_dict["playground"] = playground
        if prompt_run_settings is not UNSET:
            field_dict["prompt_run_settings"] = prompt_run_settings
        if prompt_model is not UNSET:
            field_dict["prompt_model"] = prompt_model
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if tags is not UNSET:
            field_dict["tags"] = tags
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.experiment_dataset import ExperimentDataset
        from ..models.experiment_playground import ExperimentPlayground
        from ..models.experiment_prompt import ExperimentPrompt
        from ..models.experiment_response_aggregate_feedback import ExperimentResponseAggregateFeedback
        from ..models.experiment_response_aggregate_metrics import ExperimentResponseAggregateMetrics
        from ..models.experiment_response_rating_aggregates import ExperimentResponseRatingAggregates
        from ..models.experiment_response_structured_aggregate_metrics_type_0 import (
            ExperimentResponseStructuredAggregateMetricsType0,
        )
        from ..models.experiment_response_tags import ExperimentResponseTags
        from ..models.experiment_status import ExperimentStatus
        from ..models.prompt_run_settings_output import PromptRunSettingsOutput
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        task_type = TaskType(d.pop("task_type"))

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        name = d.pop("name", UNSET)

        def _parse_created_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_created_by_user(data: object) -> None | Unset | UserInfo:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_user_type_0 = UserInfo.from_dict(data)

                return created_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | UserInfo, data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user", UNSET))

        def _parse_num_spans(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_spans = _parse_num_spans(d.pop("num_spans", UNSET))

        def _parse_num_traces(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_traces = _parse_num_traces(d.pop("num_traces", UNSET))

        def _parse_dataset(data: object) -> ExperimentDataset | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_type_0 = ExperimentDataset.from_dict(data)

                return dataset_type_0
            except:  # noqa: E722
                pass
            return cast(ExperimentDataset | None | Unset, data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        _aggregate_metrics = d.pop("aggregate_metrics", UNSET)
        aggregate_metrics: ExperimentResponseAggregateMetrics | Unset
        if isinstance(_aggregate_metrics, Unset):
            aggregate_metrics = UNSET
        else:
            aggregate_metrics = ExperimentResponseAggregateMetrics.from_dict(_aggregate_metrics)

        def _parse_structured_aggregate_metrics(
            data: object,
        ) -> ExperimentResponseStructuredAggregateMetricsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                structured_aggregate_metrics_type_0 = ExperimentResponseStructuredAggregateMetricsType0.from_dict(data)

                return structured_aggregate_metrics_type_0
            except:  # noqa: E722
                pass
            return cast(ExperimentResponseStructuredAggregateMetricsType0 | None | Unset, data)

        structured_aggregate_metrics = _parse_structured_aggregate_metrics(d.pop("structured_aggregate_metrics", UNSET))

        _aggregate_feedback = d.pop("aggregate_feedback", UNSET)
        aggregate_feedback: ExperimentResponseAggregateFeedback | Unset
        if isinstance(_aggregate_feedback, Unset):
            aggregate_feedback = UNSET
        else:
            aggregate_feedback = ExperimentResponseAggregateFeedback.from_dict(_aggregate_feedback)

        _rating_aggregates = d.pop("rating_aggregates", UNSET)
        rating_aggregates: ExperimentResponseRatingAggregates | Unset
        if isinstance(_rating_aggregates, Unset):
            rating_aggregates = UNSET
        else:
            rating_aggregates = ExperimentResponseRatingAggregates.from_dict(_rating_aggregates)

        def _parse_ranking_score(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        ranking_score = _parse_ranking_score(d.pop("ranking_score", UNSET))

        def _parse_rank(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        rank = _parse_rank(d.pop("rank", UNSET))

        def _parse_winner(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        winner = _parse_winner(d.pop("winner", UNSET))

        def _parse_playground_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        playground_id = _parse_playground_id(d.pop("playground_id", UNSET))

        def _parse_playground(data: object) -> ExperimentPlayground | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                playground_type_0 = ExperimentPlayground.from_dict(data)

                return playground_type_0
            except:  # noqa: E722
                pass
            return cast(ExperimentPlayground | None | Unset, data)

        playground = _parse_playground(d.pop("playground", UNSET))

        def _parse_prompt_run_settings(data: object) -> None | PromptRunSettingsOutput | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_run_settings_type_0 = PromptRunSettingsOutput.from_dict(data)

                return prompt_run_settings_type_0
            except:  # noqa: E722
                pass
            return cast(None | PromptRunSettingsOutput | Unset, data)

        prompt_run_settings = _parse_prompt_run_settings(d.pop("prompt_run_settings", UNSET))

        def _parse_prompt_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_model = _parse_prompt_model(d.pop("prompt_model", UNSET))

        def _parse_prompt(data: object) -> ExperimentPrompt | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_type_0 = ExperimentPrompt.from_dict(data)

                return prompt_type_0
            except:  # noqa: E722
                pass
            return cast(ExperimentPrompt | None | Unset, data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        _tags = d.pop("tags", UNSET)
        tags: ExperimentResponseTags | Unset
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = ExperimentResponseTags.from_dict(_tags)

        _status = d.pop("status", UNSET)
        status: ExperimentStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExperimentStatus.from_dict(_status)

        experiment_response = cls(
            id=id,
            project_id=project_id,
            task_type=task_type,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            created_by=created_by,
            created_by_user=created_by_user,
            num_spans=num_spans,
            num_traces=num_traces,
            dataset=dataset,
            aggregate_metrics=aggregate_metrics,
            structured_aggregate_metrics=structured_aggregate_metrics,
            aggregate_feedback=aggregate_feedback,
            rating_aggregates=rating_aggregates,
            ranking_score=ranking_score,
            rank=rank,
            winner=winner,
            playground_id=playground_id,
            playground=playground,
            prompt_run_settings=prompt_run_settings,
            prompt_model=prompt_model,
            prompt=prompt,
            tags=tags,
            status=status,
        )

        experiment_response.additional_properties = d
        return experiment_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
