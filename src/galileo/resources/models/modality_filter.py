from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.modality_filter_operator import ModalityFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModalityFilter")


@_attrs_define
class ModalityFilter:
    """Filters on content modalities in scorer jobs.
    Matches if at least one of the specified modalities is present.

        Attributes:
            operator (ModalityFilterOperator):
            value (list[str] | str):
            name (Literal['modality'] | Unset):  Default: 'modality'.
    """

    operator: ModalityFilterOperator
    value: list[str] | str
    name: Literal["modality"] | Unset = "modality"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: list[str] | str
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "value": value})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operator = ModalityFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[str], data)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(list[str] | str, data)

        value = _parse_value(d.pop("value"))

        name = cast(Literal["modality"] | Unset, d.pop("name", UNSET))
        if name != "modality" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'modality', got '{name}'")

        modality_filter = cls(operator=operator, value=value, name=name)

        modality_filter.additional_properties = d
        return modality_filter

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
