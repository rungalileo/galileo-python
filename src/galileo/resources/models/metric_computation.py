from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric_computation_status import MetricComputationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_computation_value_type_4 import MetricComputationValueType4


T = TypeVar("T", bound="MetricComputation")


@_attrs_define
class MetricComputation:
    """
    Attributes:
        error_message (Union[None, Unset, str]):
        execution_time (Union[None, Unset, float]):
        status (Union[MetricComputationStatus, None, Unset]):
        value (Union['MetricComputationValueType4', None, Unset, float, int, list[Union[None, float, int, str]], str]):
    """

    error_message: Union[None, Unset, str] = UNSET
    execution_time: Union[None, Unset, float] = UNSET
    status: Union[MetricComputationStatus, None, Unset] = UNSET
    value: Union["MetricComputationValueType4", None, Unset, float, int, list[Union[None, float, int, str]], str] = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_computation_value_type_4 import MetricComputationValueType4

        error_message: Union[None, Unset, str]
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        execution_time: Union[None, Unset, float]
        if isinstance(self.execution_time, Unset):
            execution_time = UNSET
        else:
            execution_time = self.execution_time

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, MetricComputationStatus):
            status = self.status.value
        else:
            status = self.status

        value: Union[None, Unset, dict[str, Any], float, int, list[Union[None, float, int, str]], str]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, list):
            value = []
            for value_type_3_item_data in self.value:
                value_type_3_item: Union[None, float, int, str]
                value_type_3_item = value_type_3_item_data
                value.append(value_type_3_item)

        elif isinstance(self.value, MetricComputationValueType4):
            value = self.value.to_dict()
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if execution_time is not UNSET:
            field_dict["execution_time"] = execution_time
        if status is not UNSET:
            field_dict["status"] = status
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric_computation_value_type_4 import MetricComputationValueType4

        d = src_dict.copy()

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_execution_time(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        execution_time = _parse_execution_time(d.pop("execution_time", UNSET))

        def _parse_status(data: object) -> Union[MetricComputationStatus, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = MetricComputationStatus(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[MetricComputationStatus, None, Unset], data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_value(
            data: object,
        ) -> Union["MetricComputationValueType4", None, Unset, float, int, list[Union[None, float, int, str]], str]:
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

                    def _parse_value_type_3_item(data: object) -> Union[None, float, int, str]:
                        if data is None:
                            return data
                        return cast(Union[None, float, int, str], data)

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
                Union["MetricComputationValueType4", None, Unset, float, int, list[Union[None, float, int, str]], str],
                data,
            )

        value = _parse_value(d.pop("value", UNSET))

        metric_computation = cls(error_message=error_message, execution_time=execution_time, status=status, value=value)

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
