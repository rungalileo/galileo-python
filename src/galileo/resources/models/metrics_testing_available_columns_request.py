from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

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
        log_stream_id (None | str | Unset): Log stream id associated with the traces.
        experiment_id (None | str | Unset): Experiment id associated with the traces.
        metrics_testing_id (None | str | Unset): Metrics testing id associated with the traces.
        output_type (OutputTypeEnum | Unset): Enumeration of output types.
        cot_enabled (bool | Unset): Whether the metrics testing table is using chain of thought (CoT) enabled scorers.
            If True, the columns will be generated for CoT enabled scorers. Default: False.
        metric_key (str | Unset): The metric key to use for column generation (e.g., 'generated_scorer_validation' or
            'registered_scorer_validation'). Default: 'generated_scorer_validation'.
        required_scorers (list[str] | None | Unset): List of required scorer names for composite scorers. Columns will
            be generated for these scorers.
        score_type (None | str | Unset): The score type for registered scorers (e.g., 'bool', 'int', 'float', 'str').
            Used to determine the correct data_type for the column. Provided by validation result.
    """

    name: str
    log_stream_id: None | str | Unset = UNSET
    experiment_id: None | str | Unset = UNSET
    metrics_testing_id: None | str | Unset = UNSET
    output_type: OutputTypeEnum | Unset = UNSET
    cot_enabled: bool | Unset = False
    metric_key: str | Unset = "generated_scorer_validation"
    required_scorers: list[str] | None | Unset = UNSET
    score_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        log_stream_id: None | str | Unset
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: None | str | Unset
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: None | str | Unset
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        output_type: str | Unset = UNSET
        if not isinstance(self.output_type, Unset):
            output_type = self.output_type.value

        cot_enabled = self.cot_enabled

        metric_key = self.metric_key

        required_scorers: list[str] | None | Unset
        if isinstance(self.required_scorers, Unset):
            required_scorers = UNSET
        elif isinstance(self.required_scorers, list):
            required_scorers = self.required_scorers

        else:
            required_scorers = self.required_scorers

        score_type: None | str | Unset
        score_type = UNSET if isinstance(self.score_type, Unset) else self.score_type

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
        if metric_key is not UNSET:
            field_dict["metric_key"] = metric_key
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers
        if score_type is not UNSET:
            field_dict["score_type"] = score_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_log_stream_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        _output_type = d.pop("output_type", UNSET)
        output_type: OutputTypeEnum | Unset
        output_type = UNSET if isinstance(_output_type, Unset) else OutputTypeEnum(_output_type)

        cot_enabled = d.pop("cot_enabled", UNSET)

        metric_key = d.pop("metric_key", UNSET)

        def _parse_required_scorers(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        required_scorers = _parse_required_scorers(d.pop("required_scorers", UNSET))

        def _parse_score_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        score_type = _parse_score_type(d.pop("score_type", UNSET))

        metrics_testing_available_columns_request = cls(
            name=name,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            output_type=output_type,
            cot_enabled=cot_enabled,
            metric_key=metric_key,
            required_scorers=required_scorers,
            score_type=score_type,
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
