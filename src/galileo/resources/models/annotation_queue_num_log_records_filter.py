from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.annotation_queue_num_log_records_filter_operator import AnnotationQueueNumLogRecordsFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnnotationQueueNumLogRecordsFilter")


@_attrs_define
class AnnotationQueueNumLogRecordsFilter:
    """
    Attributes:
        operator (AnnotationQueueNumLogRecordsFilterOperator):
        value (float | int | list[float] | list[int]):
        name (Literal['num_log_records'] | Unset):  Default: 'num_log_records'.
    """

    operator: AnnotationQueueNumLogRecordsFilterOperator
    value: float | int | list[float] | list[int]
    name: Literal["num_log_records"] | Unset = "num_log_records"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: float | int | list[float] | list[int]
        if isinstance(self.value, list):
            value = self.value

        elif isinstance(self.value, list):
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
        operator = AnnotationQueueNumLogRecordsFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> float | int | list[float] | list[int]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_2 = cast(list[int], data)

                return value_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_3 = cast(list[float], data)

                return value_type_3
            except:  # noqa: E722
                pass
            return cast(float | int | list[float] | list[int], data)

        value = _parse_value(d.pop("value"))

        name = cast(Literal["num_log_records"] | Unset, d.pop("name", UNSET))
        if name != "num_log_records" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'num_log_records', got '{name}'")

        annotation_queue_num_log_records_filter = cls(operator=operator, value=value, name=name)

        annotation_queue_num_log_records_filter.additional_properties = d
        return annotation_queue_num_log_records_filter

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
