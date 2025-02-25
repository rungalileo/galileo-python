import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.task_type import TaskType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_summary import EditSummary
    from ..models.model_metrics import ModelMetrics
    from ..models.slice_metrics import SliceMetrics


T = TypeVar("T", bound="ProjectRunSummary")


@_attrs_define
class ProjectRunSummary:
    """
    Attributes:
        avg_samples (float):
        hard_sample_pct (float):
        id (str):
        labels (list[str]):
        metrics (ModelMetrics):
        name (str):
        num_samples (int):
        slices (list['SliceMetrics']):
        task_type (TaskType): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the database frequently.
        updated_at (datetime.datetime):
        data_edits (Union[Unset, list['EditSummary']]):
        hard_sample_metrics (Union['ModelMetrics', None, Unset]):
        num_spans (Union[None, Unset, int]):
        spans_per_class (Union[None, Unset, float]):
        spans_per_sample (Union[None, Unset, float]):
        task (Union[None, Unset, str]):
    """

    avg_samples: float
    hard_sample_pct: float
    id: str
    labels: list[str]
    metrics: "ModelMetrics"
    name: str
    num_samples: int
    slices: list["SliceMetrics"]
    task_type: TaskType
    updated_at: datetime.datetime
    data_edits: Union[Unset, list["EditSummary"]] = UNSET
    hard_sample_metrics: Union["ModelMetrics", None, Unset] = UNSET
    num_spans: Union[None, Unset, int] = UNSET
    spans_per_class: Union[None, Unset, float] = UNSET
    spans_per_sample: Union[None, Unset, float] = UNSET
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_metrics import ModelMetrics

        avg_samples = self.avg_samples

        hard_sample_pct = self.hard_sample_pct

        id = self.id

        labels = self.labels

        metrics = self.metrics.to_dict()

        name = self.name

        num_samples = self.num_samples

        slices = []
        for slices_item_data in self.slices:
            slices_item = slices_item_data.to_dict()
            slices.append(slices_item)

        task_type = self.task_type.value

        updated_at = self.updated_at.isoformat()

        data_edits: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data_edits, Unset):
            data_edits = []
            for data_edits_item_data in self.data_edits:
                data_edits_item = data_edits_item_data.to_dict()
                data_edits.append(data_edits_item)

        hard_sample_metrics: Union[None, Unset, dict[str, Any]]
        if isinstance(self.hard_sample_metrics, Unset):
            hard_sample_metrics = UNSET
        elif isinstance(self.hard_sample_metrics, ModelMetrics):
            hard_sample_metrics = self.hard_sample_metrics.to_dict()
        else:
            hard_sample_metrics = self.hard_sample_metrics

        num_spans: Union[None, Unset, int]
        if isinstance(self.num_spans, Unset):
            num_spans = UNSET
        else:
            num_spans = self.num_spans

        spans_per_class: Union[None, Unset, float]
        if isinstance(self.spans_per_class, Unset):
            spans_per_class = UNSET
        else:
            spans_per_class = self.spans_per_class

        spans_per_sample: Union[None, Unset, float]
        if isinstance(self.spans_per_sample, Unset):
            spans_per_sample = UNSET
        else:
            spans_per_sample = self.spans_per_sample

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "avg_samples": avg_samples,
                "hard_sample_pct": hard_sample_pct,
                "id": id,
                "labels": labels,
                "metrics": metrics,
                "name": name,
                "num_samples": num_samples,
                "slices": slices,
                "task_type": task_type,
                "updated_at": updated_at,
            }
        )
        if data_edits is not UNSET:
            field_dict["data_edits"] = data_edits
        if hard_sample_metrics is not UNSET:
            field_dict["hard_sample_metrics"] = hard_sample_metrics
        if num_spans is not UNSET:
            field_dict["num_spans"] = num_spans
        if spans_per_class is not UNSET:
            field_dict["spans_per_class"] = spans_per_class
        if spans_per_sample is not UNSET:
            field_dict["spans_per_sample"] = spans_per_sample
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.edit_summary import EditSummary
        from ..models.model_metrics import ModelMetrics
        from ..models.slice_metrics import SliceMetrics

        d = src_dict.copy()
        avg_samples = d.pop("avg_samples")

        hard_sample_pct = d.pop("hard_sample_pct")

        id = d.pop("id")

        labels = cast(list[str], d.pop("labels"))

        metrics = ModelMetrics.from_dict(d.pop("metrics"))

        name = d.pop("name")

        num_samples = d.pop("num_samples")

        slices = []
        _slices = d.pop("slices")
        for slices_item_data in _slices:
            slices_item = SliceMetrics.from_dict(slices_item_data)

            slices.append(slices_item)

        task_type = TaskType(d.pop("task_type"))

        updated_at = isoparse(d.pop("updated_at"))

        data_edits = []
        _data_edits = d.pop("data_edits", UNSET)
        for data_edits_item_data in _data_edits or []:
            data_edits_item = EditSummary.from_dict(data_edits_item_data)

            data_edits.append(data_edits_item)

        def _parse_hard_sample_metrics(data: object) -> Union["ModelMetrics", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                hard_sample_metrics_type_0 = ModelMetrics.from_dict(data)

                return hard_sample_metrics_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ModelMetrics", None, Unset], data)

        hard_sample_metrics = _parse_hard_sample_metrics(d.pop("hard_sample_metrics", UNSET))

        def _parse_num_spans(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_spans = _parse_num_spans(d.pop("num_spans", UNSET))

        def _parse_spans_per_class(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        spans_per_class = _parse_spans_per_class(d.pop("spans_per_class", UNSET))

        def _parse_spans_per_sample(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        spans_per_sample = _parse_spans_per_sample(d.pop("spans_per_sample", UNSET))

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        project_run_summary = cls(
            avg_samples=avg_samples,
            hard_sample_pct=hard_sample_pct,
            id=id,
            labels=labels,
            metrics=metrics,
            name=name,
            num_samples=num_samples,
            slices=slices,
            task_type=task_type,
            updated_at=updated_at,
            data_edits=data_edits,
            hard_sample_metrics=hard_sample_metrics,
            num_spans=num_spans,
            spans_per_class=spans_per_class,
            spans_per_sample=spans_per_sample,
            task=task,
        )

        project_run_summary.additional_properties = d
        return project_run_summary

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
