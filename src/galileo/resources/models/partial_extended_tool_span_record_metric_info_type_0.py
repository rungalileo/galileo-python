from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_computing import MetricComputing
    from ..models.metric_error import MetricError
    from ..models.metric_failed import MetricFailed
    from ..models.metric_not_applicable import MetricNotApplicable
    from ..models.metric_not_computed import MetricNotComputed
    from ..models.metric_pending import MetricPending
    from ..models.metric_roll_up import MetricRollUp
    from ..models.metric_success import MetricSuccess


T = TypeVar("T", bound="PartialExtendedToolSpanRecordMetricInfoType0")


@_attrs_define
class PartialExtendedToolSpanRecordMetricInfoType0:
    """ """

    additional_properties: dict[
        str,
        Union[
            "MetricComputing",
            "MetricError",
            "MetricFailed",
            "MetricNotApplicable",
            "MetricNotComputed",
            "MetricPending",
            "MetricRollUp",
            "MetricSuccess",
        ],
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_computing import MetricComputing
        from ..models.metric_error import MetricError
        from ..models.metric_failed import MetricFailed
        from ..models.metric_not_applicable import MetricNotApplicable
        from ..models.metric_not_computed import MetricNotComputed
        from ..models.metric_pending import MetricPending
        from ..models.metric_success import MetricSuccess

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(
                prop,
                (
                    MetricNotComputed,
                    MetricPending,
                    MetricComputing,
                    MetricNotApplicable,
                    MetricSuccess,
                    MetricError,
                    MetricFailed,
                ),
            ):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_computing import MetricComputing
        from ..models.metric_error import MetricError
        from ..models.metric_failed import MetricFailed
        from ..models.metric_not_applicable import MetricNotApplicable
        from ..models.metric_not_computed import MetricNotComputed
        from ..models.metric_pending import MetricPending
        from ..models.metric_roll_up import MetricRollUp
        from ..models.metric_success import MetricSuccess

        d = dict(src_dict)
        partial_extended_tool_span_record_metric_info_type_0 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union[
                "MetricComputing",
                "MetricError",
                "MetricFailed",
                "MetricNotApplicable",
                "MetricNotComputed",
                "MetricPending",
                "MetricRollUp",
                "MetricSuccess",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return MetricNotComputed.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return MetricPending.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return MetricComputing.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return MetricNotApplicable.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return MetricSuccess.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return MetricError.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return MetricFailed.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return MetricRollUp.from_dict(data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        partial_extended_tool_span_record_metric_info_type_0.additional_properties = additional_properties
        return partial_extended_tool_span_record_metric_info_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union[
        "MetricComputing",
        "MetricError",
        "MetricFailed",
        "MetricNotApplicable",
        "MetricNotComputed",
        "MetricPending",
        "MetricRollUp",
        "MetricSuccess",
    ]:
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: Union[
            "MetricComputing",
            "MetricError",
            "MetricFailed",
            "MetricNotApplicable",
            "MetricNotComputed",
            "MetricPending",
            "MetricRollUp",
            "MetricSuccess",
        ],
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
