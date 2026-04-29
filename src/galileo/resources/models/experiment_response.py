import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
    from ..models.experiment_response_tags import ExperimentResponseTags
    from ..models.experiment_status import ExperimentStatus
    from ..models.prompt_run_settings import PromptRunSettings
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="ExperimentResponse")


@_attrs_define
class ExperimentResponse:
    """
    Attributes
    ----------
        id (str): Galileo ID of the experiment
        project_id (str): Galileo ID of the project associated with this experiment
        task_type (TaskType): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the database frequently.
        created_at (Union[Unset, datetime.datetime]): Timestamp of the experiment's creation
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the trace or span's last update
        name (Union[Unset, str]): Name of the experiment Default: ''.
        created_by (Union[None, Unset, str]):
        created_by_user (Union['UserInfo', None, Unset]):
        num_spans (Union[None, Unset, int]):
        num_traces (Union[None, Unset, int]):
        dataset (Union['ExperimentDataset', None, Unset]):
        aggregate_metrics (Union[Unset, ExperimentResponseAggregateMetrics]):
        aggregate_feedback (Union[Unset, ExperimentResponseAggregateFeedback]): Aggregate feedback information related
            to the experiment (traces only)
        rating_aggregates (Union[Unset, ExperimentResponseRatingAggregates]): Annotation aggregates keyed by template ID
            and root type
        ranking_score (Union[None, Unset, float]):
        rank (Union[None, Unset, int]):
        winner (Union[None, Unset, bool]):
        playground_id (Union[None, Unset, str]):
        playground (Union['ExperimentPlayground', None, Unset]):
        prompt_run_settings (Union['PromptRunSettings', None, Unset]):
        prompt_model (Union[None, Unset, str]):
        prompt (Union['ExperimentPrompt', None, Unset]):
        tags (Union[Unset, ExperimentResponseTags]):
        status (Union[Unset, ExperimentStatus]):
    """

    id: str
    project_id: str
    task_type: TaskType
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = ""
    created_by: Union[None, Unset, str] = UNSET
    created_by_user: Union["UserInfo", None, Unset] = UNSET
    num_spans: Union[None, Unset, int] = UNSET
    num_traces: Union[None, Unset, int] = UNSET
    dataset: Union["ExperimentDataset", None, Unset] = UNSET
    aggregate_metrics: Union[Unset, "ExperimentResponseAggregateMetrics"] = UNSET
    aggregate_feedback: Union[Unset, "ExperimentResponseAggregateFeedback"] = UNSET
    rating_aggregates: Union[Unset, "ExperimentResponseRatingAggregates"] = UNSET
    ranking_score: Union[None, Unset, float] = UNSET
    rank: Union[None, Unset, int] = UNSET
    winner: Union[None, Unset, bool] = UNSET
    playground_id: Union[None, Unset, str] = UNSET
    playground: Union["ExperimentPlayground", None, Unset] = UNSET
    prompt_run_settings: Union["PromptRunSettings", None, Unset] = UNSET
    prompt_model: Union[None, Unset, str] = UNSET
    prompt: Union["ExperimentPrompt", None, Unset] = UNSET
    tags: Union[Unset, "ExperimentResponseTags"] = UNSET
    status: Union[Unset, "ExperimentStatus"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.experiment_dataset import ExperimentDataset
        from ..models.experiment_playground import ExperimentPlayground
        from ..models.experiment_prompt import ExperimentPrompt
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.user_info import UserInfo

        id = self.id

        project_id = self.project_id

        task_type = self.task_type.value

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        name = self.name

        created_by: Union[None, Unset, str]
        created_by = UNSET if isinstance(self.created_by, Unset) else self.created_by

        created_by_user: Union[None, Unset, dict[str, Any]]
        if isinstance(self.created_by_user, Unset):
            created_by_user = UNSET
        elif isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        num_spans: Union[None, Unset, int]
        num_spans = UNSET if isinstance(self.num_spans, Unset) else self.num_spans

        num_traces: Union[None, Unset, int]
        num_traces = UNSET if isinstance(self.num_traces, Unset) else self.num_traces

        dataset: Union[None, Unset, dict[str, Any]]
        if isinstance(self.dataset, Unset):
            dataset = UNSET
        elif isinstance(self.dataset, ExperimentDataset):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        aggregate_metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aggregate_metrics, Unset):
            aggregate_metrics = self.aggregate_metrics.to_dict()

        aggregate_feedback: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aggregate_feedback, Unset):
            aggregate_feedback = self.aggregate_feedback.to_dict()

        rating_aggregates: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rating_aggregates, Unset):
            rating_aggregates = self.rating_aggregates.to_dict()

        ranking_score: Union[None, Unset, float]
        ranking_score = UNSET if isinstance(self.ranking_score, Unset) else self.ranking_score

        rank: Union[None, Unset, int]
        rank = UNSET if isinstance(self.rank, Unset) else self.rank

        winner: Union[None, Unset, bool]
        winner = UNSET if isinstance(self.winner, Unset) else self.winner

        playground_id: Union[None, Unset, str]
        playground_id = UNSET if isinstance(self.playground_id, Unset) else self.playground_id

        playground: Union[None, Unset, dict[str, Any]]
        if isinstance(self.playground, Unset):
            playground = UNSET
        elif isinstance(self.playground, ExperimentPlayground):
            playground = self.playground.to_dict()
        else:
            playground = self.playground

        prompt_run_settings: Union[None, Unset, dict[str, Any]]
        if isinstance(self.prompt_run_settings, Unset):
            prompt_run_settings = UNSET
        elif isinstance(self.prompt_run_settings, PromptRunSettings):
            prompt_run_settings = self.prompt_run_settings.to_dict()
        else:
            prompt_run_settings = self.prompt_run_settings

        prompt_model: Union[None, Unset, str]
        prompt_model = UNSET if isinstance(self.prompt_model, Unset) else self.prompt_model

        prompt: Union[None, Unset, dict[str, Any]]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        elif isinstance(self.prompt, ExperimentPrompt):
            prompt = self.prompt.to_dict()
        else:
            prompt = self.prompt

        tags: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        status: Union[Unset, dict[str, Any]] = UNSET
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
        from ..models.experiment_response_tags import ExperimentResponseTags
        from ..models.experiment_status import ExperimentStatus
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        task_type = TaskType(d.pop("task_type"))

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        created_at = UNSET if isinstance(_created_at, Unset) else isoparse(_created_at)

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return isoparse(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        name = d.pop("name", UNSET)

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_created_by_user(data: object) -> Union["UserInfo", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return UserInfo.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["UserInfo", None, Unset], data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user", UNSET))

        def _parse_num_spans(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_spans = _parse_num_spans(d.pop("num_spans", UNSET))

        def _parse_num_traces(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_traces = _parse_num_traces(d.pop("num_traces", UNSET))

        def _parse_dataset(data: object) -> Union["ExperimentDataset", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExperimentDataset.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExperimentDataset", None, Unset], data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        _aggregate_metrics = d.pop("aggregate_metrics", UNSET)
        aggregate_metrics: Union[Unset, ExperimentResponseAggregateMetrics]
        if isinstance(_aggregate_metrics, Unset):
            aggregate_metrics = UNSET
        else:
            aggregate_metrics = ExperimentResponseAggregateMetrics.from_dict(_aggregate_metrics)

        _aggregate_feedback = d.pop("aggregate_feedback", UNSET)
        aggregate_feedback: Union[Unset, ExperimentResponseAggregateFeedback]
        if isinstance(_aggregate_feedback, Unset):
            aggregate_feedback = UNSET
        else:
            aggregate_feedback = ExperimentResponseAggregateFeedback.from_dict(_aggregate_feedback)

        _rating_aggregates = d.pop("rating_aggregates", UNSET)
        rating_aggregates: Union[Unset, ExperimentResponseRatingAggregates]
        if isinstance(_rating_aggregates, Unset):
            rating_aggregates = UNSET
        else:
            rating_aggregates = ExperimentResponseRatingAggregates.from_dict(_rating_aggregates)

        def _parse_ranking_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        ranking_score = _parse_ranking_score(d.pop("ranking_score", UNSET))

        def _parse_rank(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        rank = _parse_rank(d.pop("rank", UNSET))

        def _parse_winner(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        winner = _parse_winner(d.pop("winner", UNSET))

        def _parse_playground_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        playground_id = _parse_playground_id(d.pop("playground_id", UNSET))

        def _parse_playground(data: object) -> Union["ExperimentPlayground", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExperimentPlayground.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExperimentPlayground", None, Unset], data)

        playground = _parse_playground(d.pop("playground", UNSET))

        def _parse_prompt_run_settings(data: object) -> Union["PromptRunSettings", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return PromptRunSettings.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["PromptRunSettings", None, Unset], data)

        prompt_run_settings = _parse_prompt_run_settings(d.pop("prompt_run_settings", UNSET))

        def _parse_prompt_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt_model = _parse_prompt_model(d.pop("prompt_model", UNSET))

        def _parse_prompt(data: object) -> Union["ExperimentPrompt", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExperimentPrompt.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ExperimentPrompt", None, Unset], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, ExperimentResponseTags]
        tags = UNSET if isinstance(_tags, Unset) else ExperimentResponseTags.from_dict(_tags)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExperimentStatus]
        status = UNSET if isinstance(_status, Unset) else ExperimentStatus.from_dict(_status)

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
