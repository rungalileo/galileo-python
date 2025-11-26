from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.output_type_enum import OutputTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricsTestingAvailableColumnsRequest")


@_attrs_define
class MetricsTestingAvailableColumnsRequest:
    """Request to get the available columns for the metrics testing table.

    Attributes
    ----------
        name (str): Name of the metric that we are testing.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        metrics_testing_id (Union[None, Unset, str]): Metrics testing id associated with the traces.
        output_type (Union[Unset, OutputTypeEnum]): Enumeration of output types.
        cot_enabled (Union[Unset, bool]): Whether the metrics testing table is using chain of thought (CoT) enabled
            scorers. If True, the columns will be generated for CoT enabled scorers. Default: False.
    """

    name: str
    log_stream_id: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    metrics_testing_id: Union[None, Unset, str] = UNSET
    output_type: Union[Unset, OutputTypeEnum] = UNSET
    cot_enabled: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        log_stream_id: Union[None, Unset, str]
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: Union[None, Unset, str]
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: Union[None, Unset, str]
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        output_type: Union[Unset, str] = UNSET
        if not isinstance(self.output_type, Unset):
            output_type = self.output_type.value

        cot_enabled = self.cot_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if cot_enabled is not UNSET:
            field_dict["cot_enabled"] = cot_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        _output_type = d.pop("output_type", UNSET)
        output_type: Union[Unset, OutputTypeEnum]
        output_type = UNSET if isinstance(_output_type, Unset) else OutputTypeEnum(_output_type)

        cot_enabled = d.pop("cot_enabled", UNSET)

        metrics_testing_available_columns_request = cls(
            name=name,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            output_type=output_type,
            cot_enabled=cot_enabled,
        )

        metrics_testing_available_columns_request.additional_properties = d
        return metrics_testing_available_columns_request

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
