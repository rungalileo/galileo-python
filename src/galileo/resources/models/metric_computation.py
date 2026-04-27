from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_computation_value_type_4 import MetricComputationValueType4


T = TypeVar("T", bound="MetricComputation")


@_attrs_define
class MetricComputation:
    """
    Attributes:
        value (float | int | list[float | int | None | str] | MetricComputationValueType4 | None | str | Unset):
        execution_time (float | None | Unset):
        status (str | Unset):
        error_message (None | str | Unset):
    """

    value: float | int | list[float | int | None | str] | MetricComputationValueType4 | None | str | Unset = UNSET
    execution_time: float | None | Unset = UNSET
    status: str | Unset = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_computation_value_type_4 import MetricComputationValueType4

        value: dict[str, Any] | float | int | list[float | int | None | str] | None | str | Unset
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, list):
            value = []
            for value_type_3_item_data in self.value:
                value_type_3_item: float | int | None | str
                value_type_3_item = value_type_3_item_data
                value.append(value_type_3_item)

        elif isinstance(self.value, MetricComputationValueType4):
            value = self.value.to_dict()
        else:
            value = self.value

        execution_time: float | None | Unset
        if isinstance(self.execution_time, Unset):
            execution_time = UNSET
        else:
            execution_time = self.execution_time

        status = self.status

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if execution_time is not UNSET:
            field_dict["execution_time"] = execution_time
        if status is not UNSET:
            field_dict["status"] = status
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_computation_value_type_4 import MetricComputationValueType4

        d = dict(src_dict)

        def _parse_value(
            data: object,
        ) -> float | int | list[float | int | None | str] | MetricComputationValueType4 | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_3 = []
                _value_type_3 = data
                for value_type_3_item_data in _value_type_3:

                    def _parse_value_type_3_item(data: object) -> float | int | None | str:
                        if data is None:
                            return data
                        return cast(float | int | None | str, data)

                    value_type_3_item = _parse_value_type_3_item(value_type_3_item_data)

                    value_type_3.append(value_type_3_item)

                return value_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_4 = MetricComputationValueType4.from_dict(data)

                return value_type_4
            except:  # noqa: E722
                pass
            return cast(
                float | int | list[float | int | None | str] | MetricComputationValueType4 | None | str | Unset, data
            )

        value = _parse_value(d.pop("value", UNSET))

        def _parse_execution_time(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        execution_time = _parse_execution_time(d.pop("execution_time", UNSET))

        status = d.pop("status", UNSET)

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        metric_computation = cls(value=value, execution_time=execution_time, status=status, error_message=error_message)

        metric_computation.additional_properties = d
        return metric_computation

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
