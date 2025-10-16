from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.and_node import AndNode
    from ..models.filter_leaf import FilterLeaf
    from ..models.or_node import OrNode


T = TypeVar("T", bound="NotNode")


@_attrs_define
class NotNode:
    """
    Attributes
    ----------
        not_ (Union['AndNode', 'FilterLeaf', 'NotNode', 'OrNode']):
    """

    not_: Union["AndNode", "FilterLeaf", "NotNode", "OrNode"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node import AndNode
        from ..models.filter_leaf import FilterLeaf
        from ..models.or_node import OrNode

        not_: dict[str, Any]
        not_ = self.not_.to_dict() if isinstance(self.not_, (FilterLeaf, AndNode, OrNode)) else self.not_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"not": not_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node import AndNode
        from ..models.filter_leaf import FilterLeaf
        from ..models.or_node import OrNode

        d = dict(src_dict)

        def _parse_not_(data: object) -> Union["AndNode", "FilterLeaf", "NotNode", "OrNode"]:
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

        not_ = _parse_not_(d.pop("not"))

        not_node = cls(not_=not_)

        not_node.additional_properties = d
        return not_node

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
