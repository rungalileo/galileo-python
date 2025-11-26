from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditSpan")


@_attrs_define
class EditSpan:
    """
    Attributes
    ----------
        start_index (int):
        end_index (int):
        label (str):
        id (Union[None, Unset, int]):
    """

    start_index: int
    end_index: int
    label: str
    id: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_index = self.start_index

        end_index = self.end_index

        label = self.label

        id: Union[None, Unset, int]
        id = UNSET if isinstance(self.id, Unset) else self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"start_index": start_index, "end_index": end_index, "label": label})
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_index = d.pop("start_index")

        end_index = d.pop("end_index")

        label = d.pop("label")

        def _parse_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        id = _parse_id(d.pop("id", UNSET))

        edit_span = cls(start_index=start_index, end_index=end_index, label=label, id=id)

        edit_span.additional_properties = d
        return edit_span

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
