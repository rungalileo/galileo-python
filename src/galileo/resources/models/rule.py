from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.rule_operator import RuleOperator

T = TypeVar("T", bound="Rule")


@_attrs_define
class Rule:
    """
    Attributes:
        metric (str): Name of the metric.
        operator (RuleOperator):
        target_value (Union[None, float, int, list[Any], str]): Value to compare with for this metric (right hand side).
    """

    metric: str
    operator: RuleOperator
    target_value: Union[None, float, int, list[Any], str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        operator = self.operator.value

        target_value: Union[None, float, int, list[Any], str]
        if isinstance(self.target_value, list):
            target_value = self.target_value

        else:
            target_value = self.target_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"metric": metric, "operator": operator, "target_value": target_value})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        metric = d.pop("metric")

        operator = RuleOperator(d.pop("operator"))

        def _parse_target_value(data: object) -> Union[None, float, int, list[Any], str]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                target_value_type_3 = cast(list[Any], data)

                return target_value_type_3
            except:  # noqa: E722
                pass
            return cast(Union[None, float, int, list[Any], str], data)

        target_value = _parse_target_value(d.pop("target_value"))

        rule = cls(metric=metric, operator=operator, target_value=target_value)

        rule.additional_properties = d
        return rule

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
