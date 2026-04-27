from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.aggregator import Aggregator
from ..models.alert_condition_type import AlertConditionType
from ..models.operator import Operator
from ..types import UNSET, Unset

T = TypeVar("T", bound="AlertCondition")


@_attrs_define
class AlertCondition:
    """
    Attributes:
        field (str):
        aggregation (Aggregator | str):
        operator (Operator):
        value (float | int | str):
        window (int):
        filter_value (float | int | None | str | Unset):
        filter_operator (None | Operator | Unset):
        condition_type (AlertConditionType | Unset):
    """

    field: str
    aggregation: Aggregator | str
    operator: Operator
    value: float | int | str
    window: int
    filter_value: float | int | None | str | Unset = UNSET
    filter_operator: None | Operator | Unset = UNSET
    condition_type: AlertConditionType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        aggregation: str
        if isinstance(self.aggregation, Aggregator):
            aggregation = self.aggregation.value
        else:
            aggregation = self.aggregation

        operator = self.operator.value

        value: float | int | str
        value = self.value

        window = self.window

        filter_value: float | int | None | str | Unset
        if isinstance(self.filter_value, Unset):
            filter_value = UNSET
        else:
            filter_value = self.filter_value

        filter_operator: None | str | Unset
        if isinstance(self.filter_operator, Unset):
            filter_operator = UNSET
        elif isinstance(self.filter_operator, Operator):
            filter_operator = self.filter_operator.value
        else:
            filter_operator = self.filter_operator

        condition_type: str | Unset = UNSET
        if not isinstance(self.condition_type, Unset):
            condition_type = self.condition_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"field": field, "aggregation": aggregation, "operator": operator, "value": value, "window": window}
        )
        if filter_value is not UNSET:
            field_dict["filter_value"] = filter_value
        if filter_operator is not UNSET:
            field_dict["filter_operator"] = filter_operator
        if condition_type is not UNSET:
            field_dict["condition_type"] = condition_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        def _parse_aggregation(data: object) -> Aggregator | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                aggregation_type_0 = Aggregator(data)

                return aggregation_type_0
            except:  # noqa: E722
                pass
            return cast(Aggregator | str, data)

        aggregation = _parse_aggregation(d.pop("aggregation"))

        operator = Operator(d.pop("operator"))

        def _parse_value(data: object) -> float | int | str:
            return cast(float | int | str, data)

        value = _parse_value(d.pop("value"))

        window = d.pop("window")

        def _parse_filter_value(data: object) -> float | int | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | int | None | str | Unset, data)

        filter_value = _parse_filter_value(d.pop("filter_value", UNSET))

        def _parse_filter_operator(data: object) -> None | Operator | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                filter_operator_type_0 = Operator(data)

                return filter_operator_type_0
            except:  # noqa: E722
                pass
            return cast(None | Operator | Unset, data)

        filter_operator = _parse_filter_operator(d.pop("filter_operator", UNSET))

        _condition_type = d.pop("condition_type", UNSET)
        condition_type: AlertConditionType | Unset
        if isinstance(_condition_type, Unset):
            condition_type = UNSET
        else:
            condition_type = AlertConditionType(_condition_type)

        alert_condition = cls(
            field=field,
            aggregation=aggregation,
            operator=operator,
            value=value,
            window=window,
            filter_value=filter_value,
            filter_operator=filter_operator,
            condition_type=condition_type,
        )

        alert_condition.additional_properties = d
        return alert_condition

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
