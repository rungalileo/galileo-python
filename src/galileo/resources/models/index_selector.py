from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IndexSelector")


@_attrs_define
class IndexSelector:
    """Choose specific indexes to apply the bulk operation to.

    Attributes:
        indexes (list[int]):
        selector_type (Union[Literal['indexes'], Unset]):  Default: 'indexes'.
    """

    indexes: list[int]
    selector_type: Union[Literal["indexes"], Unset] = "indexes"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        indexes = self.indexes

        selector_type = self.selector_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"indexes": indexes})
        if selector_type is not UNSET:
            field_dict["selector_type"] = selector_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        indexes = cast(list[int], d.pop("indexes"))

        selector_type = cast(Union[Literal["indexes"], Unset], d.pop("selector_type", UNSET))
        if selector_type != "indexes" and not isinstance(selector_type, Unset):
            raise ValueError(f"selector_type must match const 'indexes', got '{selector_type}'")

        index_selector = cls(indexes=indexes, selector_type=selector_type)

        index_selector.additional_properties = d
        return index_selector

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
