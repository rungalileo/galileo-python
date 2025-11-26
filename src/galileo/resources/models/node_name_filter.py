from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_name_filter_operator import NodeNameFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="NodeNameFilter")


@_attrs_define
class NodeNameFilter:
    """Filters on node names in scorer jobs.

    Attributes
    ----------
        value (str):
        operator (NodeNameFilterOperator):
        name (Union[Literal['node_name'], Unset]):  Default: 'node_name'.
        filter_type (Union[Literal['string'], Unset]):  Default: 'string'.
        case_sensitive (Union[Unset, bool]):  Default: True.
    """

    value: str
    operator: NodeNameFilterOperator
    name: Union[Literal["node_name"], Unset] = "node_name"
    filter_type: Union[Literal["string"], Unset] = "string"
    case_sensitive: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        operator = self.operator.value

        name = self.name

        filter_type = self.filter_type

        case_sensitive = self.case_sensitive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value, "operator": operator})
        if name is not UNSET:
            field_dict["name"] = name
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if case_sensitive is not UNSET:
            field_dict["case_sensitive"] = case_sensitive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        operator = NodeNameFilterOperator(d.pop("operator"))

        name = cast(Union[Literal["node_name"], Unset], d.pop("name", UNSET))
        if name != "node_name" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'node_name', got '{name}'")

        filter_type = cast(Union[Literal["string"], Unset], d.pop("filter_type", UNSET))
        if filter_type != "string" and not isinstance(filter_type, Unset):
            raise ValueError(f"filter_type must match const 'string', got '{filter_type}'")

        case_sensitive = d.pop("case_sensitive", UNSET)

        node_name_filter = cls(
            value=value, operator=operator, name=name, filter_type=filter_type, case_sensitive=case_sensitive
        )

        node_name_filter.additional_properties = d
        return node_name_filter

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
