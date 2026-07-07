from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TreeChoiceNode")


@_attrs_define
class TreeChoiceNode:
    """
    Attributes:
        label (str):
        id (str):
        children (Union[Unset, list['TreeChoiceNode']]):
    """

    label: str
    id: str
    children: Union[Unset, list["TreeChoiceNode"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        id = self.id

        children: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"label": label, "id": id})
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        id = d.pop("id")

        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in _children or []:
            children_item = TreeChoiceNode.from_dict(children_item_data)

            children.append(children_item)

        tree_choice_node = cls(label=label, id=id, children=children)

        tree_choice_node.additional_properties = d
        return tree_choice_node

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
