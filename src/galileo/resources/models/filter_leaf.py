from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.raw_filter import RawFilter


T = TypeVar("T", bound="FilterLeaf")


@_attrs_define
class FilterLeaf:
    """
    Attributes
    ----------
        filter_ (RawFilter): Raw filter input. At least one of 'name' or 'column_id' is required.
            'value' is required. 'operator' and 'case_sensitive' are optional.
    """

    filter_: "RawFilter"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filter_ = self.filter_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"filter": filter_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.raw_filter import RawFilter

        d = dict(src_dict)
        filter_ = RawFilter.from_dict(d.pop("filter"))

        filter_leaf = cls(filter_=filter_)

        filter_leaf.additional_properties = d
        return filter_leaf

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
