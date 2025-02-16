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
    from ..models.metric_success import MetricSuccess


T = TypeVar("T", bound="LlmSpanWithMetricsMetrics")


@_attrs_define
class LlmSpanWithMetricsMetrics:
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
            "MetricSuccess",
        ],
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_computing import MetricComputing
        from ..models.metric_error import MetricError
        from ..models.metric_not_applicable import MetricNotApplicable
        from ..models.metric_not_computed import MetricNotComputed
        from ..models.metric_pending import MetricPending
        from ..models.metric_success import MetricSuccess

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, MetricNotComputed):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MetricPending):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MetricComputing):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MetricNotApplicable):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MetricSuccess):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MetricError):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric_computing import MetricComputing
        from ..models.metric_error import MetricError
        from ..models.metric_failed import MetricFailed
        from ..models.metric_not_applicable import MetricNotApplicable
        from ..models.metric_not_computed import MetricNotComputed
        from ..models.metric_pending import MetricPending
        from ..models.metric_success import MetricSuccess

        d = src_dict.copy()
        llm_span_with_metrics_metrics = cls()

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
                "MetricSuccess",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = MetricNotComputed.from_dict(data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_1 = MetricPending.from_dict(data)

                    return additional_property_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_2 = MetricComputing.from_dict(data)

                    return additional_property_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_3 = MetricNotApplicable.from_dict(data)

                    return additional_property_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = MetricSuccess.from_dict(data)

                    return additional_property_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_5 = MetricError.from_dict(data)

                    return additional_property_type_5
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                additional_property_type_6 = MetricFailed.from_dict(data)

                return additional_property_type_6

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        llm_span_with_metrics_metrics.additional_properties = additional_properties
        return llm_span_with_metrics_metrics

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
            "MetricSuccess",
        ],
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
