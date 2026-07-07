from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tree_choice_node import TreeChoiceNode


T = TypeVar("T", bound="TreeChoiceConstraints")


@_attrs_define
class TreeChoiceConstraints:
    """
    Attributes:
        annotation_type (Literal['tree_choice']):
        choices_tree (Union[None, Unset, list['TreeChoiceNode']]):
        choices_tree_yaml (Union[None, Unset, str]):
    """

    annotation_type: Literal["tree_choice"]
    choices_tree: Union[None, Unset, list["TreeChoiceNode"]] = UNSET
    choices_tree_yaml: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        annotation_type = self.annotation_type

        choices_tree: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.choices_tree, Unset):
            choices_tree = UNSET
        elif isinstance(self.choices_tree, list):
            choices_tree = []
            for choices_tree_type_0_item_data in self.choices_tree:
                choices_tree_type_0_item = choices_tree_type_0_item_data.to_dict()
                choices_tree.append(choices_tree_type_0_item)

        else:
            choices_tree = self.choices_tree

        choices_tree_yaml: Union[None, Unset, str]
        if isinstance(self.choices_tree_yaml, Unset):
            choices_tree_yaml = UNSET
        else:
            choices_tree_yaml = self.choices_tree_yaml

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"annotation_type": annotation_type})
        if choices_tree is not UNSET:
            field_dict["choices_tree"] = choices_tree
        if choices_tree_yaml is not UNSET:
            field_dict["choices_tree_yaml"] = choices_tree_yaml

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tree_choice_node import TreeChoiceNode

        d = dict(src_dict)
        annotation_type = cast(Literal["tree_choice"], d.pop("annotation_type"))
        if annotation_type != "tree_choice":
            raise ValueError(f"annotation_type must match const 'tree_choice', got '{annotation_type}'")

        def _parse_choices_tree(data: object) -> Union[None, Unset, list["TreeChoiceNode"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                choices_tree_type_0 = []
                _choices_tree_type_0 = data
                for choices_tree_type_0_item_data in _choices_tree_type_0:
                    choices_tree_type_0_item = TreeChoiceNode.from_dict(choices_tree_type_0_item_data)

                    choices_tree_type_0.append(choices_tree_type_0_item)

                return choices_tree_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["TreeChoiceNode"]], data)

        choices_tree = _parse_choices_tree(d.pop("choices_tree", UNSET))

        def _parse_choices_tree_yaml(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        choices_tree_yaml = _parse_choices_tree_yaml(d.pop("choices_tree_yaml", UNSET))

        tree_choice_constraints = cls(
            annotation_type=annotation_type, choices_tree=choices_tree, choices_tree_yaml=choices_tree_yaml
        )

        tree_choice_constraints.additional_properties = d
        return tree_choice_constraints

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
