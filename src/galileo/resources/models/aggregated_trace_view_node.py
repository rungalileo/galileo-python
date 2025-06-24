from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.step_type import StepType

T = TypeVar("T", bound="AggregatedTraceViewNode")


@_attrs_define
class AggregatedTraceViewNode:
    """
    Attributes:
        has_children (bool):
        id (str):
        name (Union[None, str]):
        occurrences (int):
        parent_id (Union[None, str]):
        type_ (StepType):
    """

    has_children: bool
    id: str
    name: Union[None, str]
    occurrences: int
    parent_id: Union[None, str]
    type_: StepType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_children = self.has_children

        id = self.id

        name: Union[None, str]
        name = self.name

        occurrences = self.occurrences

        parent_id: Union[None, str]
        parent_id = self.parent_id

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_children": has_children,
                "id": id,
                "name": name,
                "occurrences": occurrences,
                "parent_id": parent_id,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        has_children = d.pop("has_children")

        id = d.pop("id")

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        occurrences = d.pop("occurrences")

        def _parse_parent_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        type_ = StepType(d.pop("type"))

        aggregated_trace_view_node = cls(
            has_children=has_children, id=id, name=name, occurrences=occurrences, parent_id=parent_id, type_=type_
        )

        aggregated_trace_view_node.additional_properties = d
        return aggregated_trace_view_node

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
