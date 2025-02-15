from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_data_get_response_values import LogDataGetResponseValues


T = TypeVar("T", bound="LogDataGetResponse")


@_attrs_define
class LogDataGetResponse:
    """
    Attributes:
        values (Union[Unset, LogDataGetResponseValues]): Dictionary containing the mapping of column ids to data values.
    """

    values: Union[Unset, "LogDataGetResponseValues"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.log_data_get_response_values import LogDataGetResponseValues

        d = src_dict.copy()
        _values = d.pop("values", UNSET)
        values: Union[Unset, LogDataGetResponseValues]
        if isinstance(_values, Unset):
            values = UNSET
        else:
            values = LogDataGetResponseValues.from_dict(_values)

        log_data_get_response = cls(
            values=values,
        )

        log_data_get_response.additional_properties = d
        return log_data_get_response

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
