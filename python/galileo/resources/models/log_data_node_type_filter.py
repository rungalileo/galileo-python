from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.log_data_node_type_filter_operator import LogDataNodeTypeFilterOperator
from ..models.node_type import NodeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LogDataNodeTypeFilter")


@_attrs_define
class LogDataNodeTypeFilter:
    """
    Attributes:
        operator (LogDataNodeTypeFilterOperator):
        value (Union[NodeType, list[NodeType]]):
        name (Union[Literal['node_type'], Unset]):  Default: 'node_type'.
    """

    operator: LogDataNodeTypeFilterOperator
    value: Union[NodeType, list[NodeType]]
    name: Union[Literal["node_type"], Unset] = "node_type"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: Union[list[str], str]
        if isinstance(self.value, NodeType):
            value = self.value.value
        else:
            value = []
            for value_type_1_item_data in self.value:
                value_type_1_item = value_type_1_item_data.value
                value.append(value_type_1_item)

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "value": value})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        operator = LogDataNodeTypeFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[NodeType, list[NodeType]]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                value_type_0 = NodeType(data)

                return value_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            value_type_1 = []
            _value_type_1 = data
            for value_type_1_item_data in _value_type_1:
                value_type_1_item = NodeType(value_type_1_item_data)

                value_type_1.append(value_type_1_item)

            return value_type_1

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["node_type"], Unset], d.pop("name", UNSET))
        if name != "node_type" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'node_type', got '{name}'")

        log_data_node_type_filter = cls(operator=operator, value=value, name=name)

        log_data_node_type_filter.additional_properties = d
        return log_data_node_type_filter

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
