from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.filter_leaf import FilterLeaf
    from ..models.not_node import NotNode
    from ..models.or_node import OrNode


T = TypeVar("T", bound="AndNode")


@_attrs_define
class AndNode:
    """
    Attributes
    ----------
        and_ (list[Union['AndNode', 'FilterLeaf', 'NotNode', 'OrNode']]):
    """

    and_: list[Union["AndNode", "FilterLeaf", "NotNode", "OrNode"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.filter_leaf import FilterLeaf
        from ..models.or_node import OrNode

        and_ = []
        for and_item_data in self.and_:
            and_item: dict[str, Any]
            if isinstance(and_item_data, (FilterLeaf, AndNode, OrNode)):
                and_item = and_item_data.to_dict()
            else:
                and_item = and_item_data.to_dict()

            and_.append(and_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"and": and_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_leaf import FilterLeaf
        from ..models.not_node import NotNode
        from ..models.or_node import OrNode

        d = dict(src_dict)
        and_ = []
        _and_ = d.pop("and")
        for and_item_data in _and_:

            def _parse_and_item(data: object) -> Union["AndNode", "FilterLeaf", "NotNode", "OrNode"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return FilterLeaf.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return AndNode.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return OrNode.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return NotNode.from_dict(data)

            and_item = _parse_and_item(and_item_data)

            and_.append(and_item)

        and_node = cls(and_=and_)

        and_node.additional_properties = d
        return and_node

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
