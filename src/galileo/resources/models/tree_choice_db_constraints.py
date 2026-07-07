from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.tree_choice_node import TreeChoiceNode


T = TypeVar("T", bound="TreeChoiceDBConstraints")


@_attrs_define
class TreeChoiceDBConstraints:
    """
    Attributes:
        annotation_type (Literal['tree_choice']):
        choices_tree (list['TreeChoiceNode']):
        choices_tree_yaml (str):
    """

    annotation_type: Literal["tree_choice"]
    choices_tree: list["TreeChoiceNode"]
    choices_tree_yaml: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        annotation_type = self.annotation_type

        choices_tree = []
        for choices_tree_item_data in self.choices_tree:
            choices_tree_item = choices_tree_item_data.to_dict()
            choices_tree.append(choices_tree_item)

        choices_tree_yaml = self.choices_tree_yaml

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"annotation_type": annotation_type, "choices_tree": choices_tree, "choices_tree_yaml": choices_tree_yaml}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tree_choice_node import TreeChoiceNode

        d = dict(src_dict)
        annotation_type = cast(Literal["tree_choice"], d.pop("annotation_type"))
        if annotation_type != "tree_choice":
            raise ValueError(f"annotation_type must match const 'tree_choice', got '{annotation_type}'")

        choices_tree = []
        _choices_tree = d.pop("choices_tree")
        for choices_tree_item_data in _choices_tree:
            choices_tree_item = TreeChoiceNode.from_dict(choices_tree_item_data)

            choices_tree.append(choices_tree_item)

        choices_tree_yaml = d.pop("choices_tree_yaml")

        tree_choice_db_constraints = cls(
            annotation_type=annotation_type, choices_tree=choices_tree, choices_tree_yaml=choices_tree_yaml
        )

        tree_choice_db_constraints.additional_properties = d
        return tree_choice_db_constraints

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
