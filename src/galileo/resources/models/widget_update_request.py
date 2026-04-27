from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric_aggregation import MetricAggregation
from ..models.widget_type import WidgetType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.widget_update_request_dataset_type_0_item import WidgetUpdateRequestDatasetType0Item


T = TypeVar("T", bound="WidgetUpdateRequest")


@_attrs_define
class WidgetUpdateRequest:
    """
    Attributes:
        name (None | str | Unset):
        description (None | str | Unset):
        type_ (None | Unset | WidgetType):
        dataset (list[WidgetUpdateRequestDatasetType0Item] | None | Unset):
        metric (None | str | Unset):
        aggregation (MetricAggregation | None | Unset):
        section_id (None | str | Unset):
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    type_: None | Unset | WidgetType = UNSET
    dataset: list[WidgetUpdateRequestDatasetType0Item] | None | Unset = UNSET
    metric: None | str | Unset = UNSET
    aggregation: MetricAggregation | None | Unset = UNSET
    section_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, WidgetType):
            type_ = self.type_.value
        else:
            type_ = self.type_

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

        metric: None | str | Unset
        if isinstance(self.metric, Unset):
            metric = UNSET
        else:
            metric = self.metric

        aggregation: None | str | Unset
        if isinstance(self.aggregation, Unset):
            aggregation = UNSET
        elif isinstance(self.aggregation, MetricAggregation):
            aggregation = self.aggregation.value
        else:
            aggregation = self.aggregation

        section_id: None | str | Unset
        if isinstance(self.section_id, Unset):
            section_id = UNSET
        else:
            section_id = self.section_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if metric is not UNSET:
            field_dict["metric"] = metric
        if aggregation is not UNSET:
            field_dict["aggregation"] = aggregation
        if section_id is not UNSET:
            field_dict["section_id"] = section_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.widget_update_request_dataset_type_0_item import WidgetUpdateRequestDatasetType0Item

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_type_(data: object) -> None | Unset | WidgetType:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = WidgetType(data)

                return type_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | WidgetType, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_dataset(data: object) -> list[WidgetUpdateRequestDatasetType0Item] | None | Unset:
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
                    dataset_type_0_item = WidgetUpdateRequestDatasetType0Item.from_dict(dataset_type_0_item_data)

                    dataset_type_0.append(dataset_type_0_item)

                return dataset_type_0
            except:  # noqa: E722
                pass
            return cast(list[WidgetUpdateRequestDatasetType0Item] | None | Unset, data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        def _parse_metric(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metric = _parse_metric(d.pop("metric", UNSET))

        def _parse_aggregation(data: object) -> MetricAggregation | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                aggregation_type_0 = MetricAggregation(data)

                return aggregation_type_0
            except:  # noqa: E722
                pass
            return cast(MetricAggregation | None | Unset, data)

        aggregation = _parse_aggregation(d.pop("aggregation", UNSET))

        def _parse_section_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        section_id = _parse_section_id(d.pop("section_id", UNSET))

        widget_update_request = cls(
            name=name,
            description=description,
            type_=type_,
            dataset=dataset,
            metric=metric,
            aggregation=aggregation,
            section_id=section_id,
        )

        widget_update_request.additional_properties = d
        return widget_update_request

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
