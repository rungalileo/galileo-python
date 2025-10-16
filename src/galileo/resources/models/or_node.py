from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.and_node import AndNode
    from ..models.filter_leaf import FilterLeaf
    from ..models.not_node import NotNode


T = TypeVar("T", bound="OrNode")


@_attrs_define
class OrNode:
    """
    Attributes
    ----------
        or_ (list[Union['AndNode', 'FilterLeaf', 'NotNode', 'OrNode']]):
    """

    or_: list[Union["AndNode", "FilterLeaf", "NotNode", "OrNode"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node import AndNode
        from ..models.filter_leaf import FilterLeaf

        or_ = []
        for or_item_data in self.or_:
            or_item: dict[str, Any]
            if isinstance(or_item_data, (FilterLeaf, AndNode, OrNode)):
                or_item = or_item_data.to_dict()
            else:
                or_item = or_item_data.to_dict()

            or_.append(or_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"or": or_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node import AndNode
        from ..models.filter_leaf import FilterLeaf
        from ..models.not_node import NotNode

        d = dict(src_dict)
        or_ = []
        _or_ = d.pop("or")
        for or_item_data in _or_:

            def _parse_or_item(data: object) -> Union["AndNode", "FilterLeaf", "NotNode", "OrNode"]:
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

            or_item = _parse_or_item(or_item_data)

            or_.append(or_item)

        or_node = cls(or_=or_)

        or_node.additional_properties = d
        return or_node

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
