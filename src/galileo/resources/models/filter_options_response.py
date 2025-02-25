from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_options_response_filter_options import FilterOptionsResponseFilterOptions


T = TypeVar("T", bound="FilterOptionsResponse")


@_attrs_define
class FilterOptionsResponse:
    """
    Attributes:
        filter_options (Union[Unset, FilterOptionsResponseFilterOptions]):
    """

    filter_options: Union[Unset, "FilterOptionsResponseFilterOptions"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filter_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_options, Unset):
            filter_options = self.filter_options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_options is not UNSET:
            field_dict["filter_options"] = filter_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.filter_options_response_filter_options import FilterOptionsResponseFilterOptions

        d = src_dict.copy()
        _filter_options = d.pop("filter_options", UNSET)
        filter_options: Union[Unset, FilterOptionsResponseFilterOptions]
        if isinstance(_filter_options, Unset):
            filter_options = UNSET
        else:
            filter_options = FilterOptionsResponseFilterOptions.from_dict(_filter_options)

        filter_options_response = cls(filter_options=filter_options)

        filter_options_response.additional_properties = d
        return filter_options_response

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
