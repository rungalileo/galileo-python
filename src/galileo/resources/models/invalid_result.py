from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InvalidResult")


@_attrs_define
class InvalidResult:
    """
    Attributes
    ----------
        error_message (str):
        result_type (Union[Literal['invalid'], Unset]):  Default: 'invalid'.
    """

    error_message: str
    result_type: Union[Literal["invalid"], Unset] = "invalid"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error_message = self.error_message

        result_type = self.result_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"error_message": error_message})
        if result_type is not UNSET:
            field_dict["result_type"] = result_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error_message = d.pop("error_message")

        result_type = cast(Union[Literal["invalid"], Unset], d.pop("result_type", UNSET))
        if result_type != "invalid" and not isinstance(result_type, Unset):
            raise ValueError(f"result_type must match const 'invalid', got '{result_type}'")

        invalid_result = cls(error_message=error_message, result_type=result_type)

        invalid_result.additional_properties = d
        return invalid_result

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
