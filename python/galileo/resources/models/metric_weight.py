from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.group_label import GroupLabel
from ..models.metric_descriptions import MetricDescriptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricWeight")


@_attrs_define
class MetricWeight:
    """
    Attributes:
        description (Union[MetricDescriptions, None, Unset]):
        group_label (Union[GroupLabel, None, Unset]):
        label (Union[None, Unset, str]):
        weight (Union[Unset, float]):  Default: 0.5.
    """

    description: Union[MetricDescriptions, None, Unset] = UNSET
    group_label: Union[GroupLabel, None, Unset] = UNSET
    label: Union[None, Unset, str] = UNSET
    weight: Union[Unset, float] = 0.5
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, MetricDescriptions):
            description = self.description.value
        else:
            description = self.description

        group_label: Union[None, Unset, str]
        if isinstance(self.group_label, Unset):
            group_label = UNSET
        elif isinstance(self.group_label, GroupLabel):
            group_label = self.group_label.value
        else:
            group_label = self.group_label

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if group_label is not UNSET:
            field_dict["group_label"] = group_label
        if label is not UNSET:
            field_dict["label"] = label
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_description(data: object) -> Union[MetricDescriptions, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                description_type_0 = MetricDescriptions(data)

                return description_type_0
            except:  # noqa: E722
                pass
            return cast(Union[MetricDescriptions, None, Unset], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_group_label(data: object) -> Union[GroupLabel, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                group_label_type_0 = GroupLabel(data)

                return group_label_type_0
            except:  # noqa: E722
                pass
            return cast(Union[GroupLabel, None, Unset], data)

        group_label = _parse_group_label(d.pop("group_label", UNSET))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        weight = d.pop("weight", UNSET)

        metric_weight = cls(description=description, group_label=group_label, label=label, weight=weight)

        metric_weight.additional_properties = d
        return metric_weight

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
