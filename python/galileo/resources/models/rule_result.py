from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_status import ExecutionStatus
from ..models.rule_operator import RuleOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="RuleResult")


@_attrs_define
class RuleResult:
    """
    Attributes:
        metric (str): Name of the metric.
        operator (RuleOperator):
        target_value (Union[None, float, int, list[Any], str]): Value to compare with for this metric (right hand side).
        execution_time (Union[None, Unset, float]): Execution time for the rule in seconds.
        status (Union[Unset, ExecutionStatus]): Status of the execution.
        value (Union[Any, None, Unset]): Result of the metric computation.
    """

    metric: str
    operator: RuleOperator
    target_value: Union[None, float, int, list[Any], str]
    execution_time: Union[None, Unset, float] = UNSET
    status: Union[Unset, ExecutionStatus] = UNSET
    value: Union[Any, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        operator = self.operator.value

        target_value: Union[None, float, int, list[Any], str]
        if isinstance(self.target_value, list):
            target_value = self.target_value

        else:
            target_value = self.target_value

        execution_time: Union[None, Unset, float]
        if isinstance(self.execution_time, Unset):
            execution_time = UNSET
        else:
            execution_time = self.execution_time

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        value: Union[Any, None, Unset]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"metric": metric, "operator": operator, "target_value": target_value})
        if execution_time is not UNSET:
            field_dict["execution_time"] = execution_time
        if status is not UNSET:
            field_dict["status"] = status
        if value is not UNSET:
            field_dict["value"] = value

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

        def _parse_execution_time(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        execution_time = _parse_execution_time(d.pop("execution_time", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExecutionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExecutionStatus(_status)

        def _parse_value(data: object) -> Union[Any, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, None, Unset], data)

        value = _parse_value(d.pop("value", UNSET))

        rule_result = cls(
            metric=metric,
            operator=operator,
            target_value=target_value,
            execution_time=execution_time,
            status=status,
            value=value,
        )

        rule_result.additional_properties = d
        return rule_result

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
