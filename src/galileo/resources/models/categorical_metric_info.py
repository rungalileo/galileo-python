from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.categorical_metric_info_category_counts import CategoricalMetricInfoCategoryCounts


T = TypeVar("T", bound="CategoricalMetricInfo")


@_attrs_define
class CategoricalMetricInfo:
    """
    Attributes:
        name (str): Unique identifier for the metric
        label (str): Human-readable display name for the metric
        aggregation_type (Union[Literal['categorical'], Unset]): Discriminator: categorical metrics aggregated as per-
            label counts Default: 'categorical'.
        category_counts (Union[Unset, CategoricalMetricInfoCategoryCounts]): Count of occurrences per category label
            across records
    """

    name: str
    label: str
    aggregation_type: Union[Literal["categorical"], Unset] = "categorical"
    category_counts: Union[Unset, "CategoricalMetricInfoCategoryCounts"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        label = self.label

        aggregation_type = self.aggregation_type

        category_counts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.category_counts, Unset):
            category_counts = self.category_counts.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "label": label})
        if aggregation_type is not UNSET:
            field_dict["aggregation_type"] = aggregation_type
        if category_counts is not UNSET:
            field_dict["category_counts"] = category_counts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.categorical_metric_info_category_counts import CategoricalMetricInfoCategoryCounts

        d = dict(src_dict)
        name = d.pop("name")

        label = d.pop("label")

        aggregation_type = cast(Union[Literal["categorical"], Unset], d.pop("aggregation_type", UNSET))
        if aggregation_type != "categorical" and not isinstance(aggregation_type, Unset):
            raise ValueError(f"aggregation_type must match const 'categorical', got '{aggregation_type}'")

        _category_counts = d.pop("category_counts", UNSET)
        category_counts: Union[Unset, CategoricalMetricInfoCategoryCounts]
        if isinstance(_category_counts, Unset):
            category_counts = UNSET
        else:
            category_counts = CategoricalMetricInfoCategoryCounts.from_dict(_category_counts)

        categorical_metric_info = cls(
            name=name, label=label, aggregation_type=aggregation_type, category_counts=category_counts
        )

        categorical_metric_info.additional_properties = d
        return categorical_metric_info

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
