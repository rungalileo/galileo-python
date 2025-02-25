from typing import Any, TypeVar, Union, cast

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
        aggregation (Union[Aggregator, str]):
        field (str):
        operator (Operator):
        value (Union[float, int, str]):
        window (int):
        condition_type (Union[Unset, AlertConditionType]):
        filter_operator (Union[None, Operator, Unset]):
        filter_value (Union[None, Unset, float, int, str]):
    """

    aggregation: Union[Aggregator, str]
    field: str
    operator: Operator
    value: Union[float, int, str]
    window: int
    condition_type: Union[Unset, AlertConditionType] = UNSET
    filter_operator: Union[None, Operator, Unset] = UNSET
    filter_value: Union[None, Unset, float, int, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aggregation: str
        if isinstance(self.aggregation, Aggregator):
            aggregation = self.aggregation.value
        else:
            aggregation = self.aggregation

        field = self.field

        operator = self.operator.value

        value: Union[float, int, str]
        value = self.value

        window = self.window

        condition_type: Union[Unset, str] = UNSET
        if not isinstance(self.condition_type, Unset):
            condition_type = self.condition_type.value

        filter_operator: Union[None, Unset, str]
        if isinstance(self.filter_operator, Unset):
            filter_operator = UNSET
        elif isinstance(self.filter_operator, Operator):
            filter_operator = self.filter_operator.value
        else:
            filter_operator = self.filter_operator

        filter_value: Union[None, Unset, float, int, str]
        if isinstance(self.filter_value, Unset):
            filter_value = UNSET
        else:
            filter_value = self.filter_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"aggregation": aggregation, "field": field, "operator": operator, "value": value, "window": window}
        )
        if condition_type is not UNSET:
            field_dict["condition_type"] = condition_type
        if filter_operator is not UNSET:
            field_dict["filter_operator"] = filter_operator
        if filter_value is not UNSET:
            field_dict["filter_value"] = filter_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_aggregation(data: object) -> Union[Aggregator, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                aggregation_type_0 = Aggregator(data)

                return aggregation_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Aggregator, str], data)

        aggregation = _parse_aggregation(d.pop("aggregation"))

        field = d.pop("field")

        operator = Operator(d.pop("operator"))

        def _parse_value(data: object) -> Union[float, int, str]:
            return cast(Union[float, int, str], data)

        value = _parse_value(d.pop("value"))

        window = d.pop("window")

        _condition_type = d.pop("condition_type", UNSET)
        condition_type: Union[Unset, AlertConditionType]
        if isinstance(_condition_type, Unset):
            condition_type = UNSET
        else:
            condition_type = AlertConditionType(_condition_type)

        def _parse_filter_operator(data: object) -> Union[None, Operator, Unset]:
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
            return cast(Union[None, Operator, Unset], data)

        filter_operator = _parse_filter_operator(d.pop("filter_operator", UNSET))

        def _parse_filter_value(data: object) -> Union[None, Unset, float, int, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float, int, str], data)

        filter_value = _parse_filter_value(d.pop("filter_value", UNSET))

        alert_condition = cls(
            aggregation=aggregation,
            field=field,
            operator=operator,
            value=value,
            window=window,
            condition_type=condition_type,
            filter_operator=filter_operator,
            filter_value=filter_value,
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
