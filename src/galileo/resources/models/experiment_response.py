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
    from ..models.experiment_response_aggregate_feedback import ExperimentResponseAggregateFeedback
    from ..models.experiment_response_aggregate_metrics import ExperimentResponseAggregateMetrics


T = TypeVar("T", bound="ExperimentResponse")


@_attrs_define
class ExperimentResponse:
    """
    Attributes:
        id (str): Galileo ID of the experiment
        project_id (str): Galileo ID of the project associated with this experiment
        task_type (TaskType): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the database frequently.
        aggregate_feedback (Union[Unset, ExperimentResponseAggregateFeedback]): Aggregate feedback information related
            to the experiment
        aggregate_metrics (Union[Unset, ExperimentResponseAggregateMetrics]):
        created_at (Union[Unset, datetime.datetime]): Timestamp of the experiment's creation
        created_by (Union[None, Unset, str]):
        dataset (Union['ExperimentDataset', None, Unset]):
        name (Union[Unset, str]): Name of the experiment Default: ''.
        rank (Union[None, Unset, int]):
        ranking_score (Union[None, Unset, float]):
        updated_at (Union[None, Unset, datetime.datetime]): Timestamp of the trace or span's last update
        winner (Union[None, Unset, bool]):
    """

    id: str
    project_id: str
    task_type: TaskType
    aggregate_feedback: Union[Unset, "ExperimentResponseAggregateFeedback"] = UNSET
    aggregate_metrics: Union[Unset, "ExperimentResponseAggregateMetrics"] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    dataset: Union["ExperimentDataset", None, Unset] = UNSET
    name: Union[Unset, str] = ""
    rank: Union[None, Unset, int] = UNSET
    ranking_score: Union[None, Unset, float] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    winner: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.experiment_dataset import ExperimentDataset

        id = self.id

        project_id = self.project_id

        task_type = self.task_type.value

        aggregate_feedback: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aggregate_feedback, Unset):
            aggregate_feedback = self.aggregate_feedback.to_dict()

        aggregate_metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aggregate_metrics, Unset):
            aggregate_metrics = self.aggregate_metrics.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        dataset: Union[None, Unset, dict[str, Any]]
        if isinstance(self.dataset, Unset):
            dataset = UNSET
        elif isinstance(self.dataset, ExperimentDataset):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        name = self.name

        rank: Union[None, Unset, int]
        if isinstance(self.rank, Unset):
            rank = UNSET
        else:
            rank = self.rank

        ranking_score: Union[None, Unset, float]
        if isinstance(self.ranking_score, Unset):
            ranking_score = UNSET
        else:
            ranking_score = self.ranking_score

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        winner: Union[None, Unset, bool]
        if isinstance(self.winner, Unset):
            winner = UNSET
        else:
            winner = self.winner

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "project_id": project_id, "task_type": task_type})
        if aggregate_feedback is not UNSET:
            field_dict["aggregate_feedback"] = aggregate_feedback
        if aggregate_metrics is not UNSET:
            field_dict["aggregate_metrics"] = aggregate_metrics
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if name is not UNSET:
            field_dict["name"] = name
        if rank is not UNSET:
            field_dict["rank"] = rank
        if ranking_score is not UNSET:
            field_dict["ranking_score"] = ranking_score
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if winner is not UNSET:
            field_dict["winner"] = winner

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.experiment_dataset import ExperimentDataset
        from ..models.experiment_response_aggregate_feedback import ExperimentResponseAggregateFeedback
        from ..models.experiment_response_aggregate_metrics import ExperimentResponseAggregateMetrics

        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        task_type = TaskType(d.pop("task_type"))

        _aggregate_feedback = d.pop("aggregate_feedback", UNSET)
        aggregate_feedback: Union[Unset, ExperimentResponseAggregateFeedback]
        if isinstance(_aggregate_feedback, Unset):
            aggregate_feedback = UNSET
        else:
            aggregate_feedback = ExperimentResponseAggregateFeedback.from_dict(_aggregate_feedback)

        _aggregate_metrics = d.pop("aggregate_metrics", UNSET)
        aggregate_metrics: Union[Unset, ExperimentResponseAggregateMetrics]
        if isinstance(_aggregate_metrics, Unset):
            aggregate_metrics = UNSET
        else:
            aggregate_metrics = ExperimentResponseAggregateMetrics.from_dict(_aggregate_metrics)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_dataset(data: object) -> Union["ExperimentDataset", None, Unset]:
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
            return cast(Union["ExperimentDataset", None, Unset], data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        name = d.pop("name", UNSET)

        def _parse_rank(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        rank = _parse_rank(d.pop("rank", UNSET))

        def _parse_ranking_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        ranking_score = _parse_ranking_score(d.pop("ranking_score", UNSET))

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
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
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_winner(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        winner = _parse_winner(d.pop("winner", UNSET))

        experiment_response = cls(
            id=id,
            project_id=project_id,
            task_type=task_type,
            aggregate_feedback=aggregate_feedback,
            aggregate_metrics=aggregate_metrics,
            created_at=created_at,
            created_by=created_by,
            dataset=dataset,
            name=name,
            rank=rank,
            ranking_score=ranking_score,
            updated_at=updated_at,
            winner=winner,
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
