from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric_aggregation import MetricAggregation
from ..models.widget_type import WidgetType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.widget_response_dataset_type_0_item import WidgetResponseDatasetType0Item


T = TypeVar("T", bound="WidgetResponse")


@_attrs_define
class WidgetResponse:
    """
    Attributes:
        id (str):
        name (str):
        type_ (WidgetType):
        metric (str):
        aggregation (MetricAggregation):
        description (None | str | Unset):
        dataset (list[WidgetResponseDatasetType0Item] | None | Unset):
        section_id (None | str | Unset):
    """

    id: str
    name: str
    type_: WidgetType
    metric: str
    aggregation: MetricAggregation
    description: None | str | Unset = UNSET
    dataset: list[WidgetResponseDatasetType0Item] | None | Unset = UNSET
    section_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        type_ = self.type_.value

        metric = self.metric

        aggregation = self.aggregation.value

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        dataset: list[dict[str, Any]] | None | Unset
        if isinstance(self.dataset, Unset):
            dataset = UNSET
        elif isinstance(self.dataset, list):
            dataset = []
            for dataset_type_0_item_data in self.dataset:
                dataset_type_0_item = dataset_type_0_item_data.to_dict()
                dataset.append(dataset_type_0_item)

        else:
            dataset = self.dataset

        section_id: None | str | Unset
        if isinstance(self.section_id, Unset):
            section_id = UNSET
        else:
            section_id = self.section_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "name": name, "type": type_, "metric": metric, "aggregation": aggregation})
        if description is not UNSET:
            field_dict["description"] = description
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if section_id is not UNSET:
            field_dict["section_id"] = section_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.widget_response_dataset_type_0_item import WidgetResponseDatasetType0Item

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        type_ = WidgetType(d.pop("type"))

        metric = d.pop("metric")

        aggregation = MetricAggregation(d.pop("aggregation"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_dataset(data: object) -> list[WidgetResponseDatasetType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                dataset_type_0 = []
                _dataset_type_0 = data
                for dataset_type_0_item_data in _dataset_type_0:
                    dataset_type_0_item = WidgetResponseDatasetType0Item.from_dict(dataset_type_0_item_data)

                    dataset_type_0.append(dataset_type_0_item)

                return dataset_type_0
            except:  # noqa: E722
                pass
            return cast(list[WidgetResponseDatasetType0Item] | None | Unset, data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        def _parse_section_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        section_id = _parse_section_id(d.pop("section_id", UNSET))

        widget_response = cls(
            id=id,
            name=name,
            type_=type_,
            metric=metric,
            aggregation=aggregation,
            description=description,
            dataset=dataset,
            section_id=section_id,
        )

        widget_response.additional_properties = d
        return widget_response

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
