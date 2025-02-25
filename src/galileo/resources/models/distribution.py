from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.group_by_metrics import GroupByMetrics


T = TypeVar("T", bound="Distribution")


@_attrs_define
class Distribution:
    """A distribution histogram for a run/filter for a particular numerical column.

    bins are boundaries for the x axis and counts are the y axis. bins will have 1 more value than counts because the
    count at index i is for the range [bin[i], bin[i+1]), with the lower boundary inclusive and the upper boundary
    exclusive

        Attributes:
            bins (list[float]):
            counts (list[int]):
            metrics (Union['GroupByMetrics', None, Unset]):
    """

    bins: list[float]
    counts: list[int]
    metrics: Union["GroupByMetrics", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.group_by_metrics import GroupByMetrics

        bins = self.bins

        counts = self.counts

        metrics: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metrics, Unset):
            metrics = UNSET
        elif isinstance(self.metrics, GroupByMetrics):
            metrics = self.metrics.to_dict()
        else:
            metrics = self.metrics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"bins": bins, "counts": counts})
        if metrics is not UNSET:
            field_dict["metrics"] = metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.group_by_metrics import GroupByMetrics

        d = src_dict.copy()
        bins = cast(list[float], d.pop("bins"))

        counts = cast(list[int], d.pop("counts"))

        def _parse_metrics(data: object) -> Union["GroupByMetrics", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metrics_type_0 = GroupByMetrics.from_dict(data)

                return metrics_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GroupByMetrics", None, Unset], data)

        metrics = _parse_metrics(d.pop("metrics", UNSET))

        distribution = cls(bins=bins, counts=counts, metrics=metrics)

        distribution.additional_properties = d
        return distribution

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
