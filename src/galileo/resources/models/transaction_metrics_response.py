from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.aggregate_metrics import AggregateMetrics
    from ..models.transaction_metrics_response_bucketed_metrics import TransactionMetricsResponseBucketedMetrics


T = TypeVar("T", bound="TransactionMetricsResponse")


@_attrs_define
class TransactionMetricsResponse:
    """
    Attributes:
        aggregate_metrics (AggregateMetrics):
        bucketed_metrics (TransactionMetricsResponseBucketedMetrics):
        group_by_columns (list[str]):
    """

    aggregate_metrics: "AggregateMetrics"
    bucketed_metrics: "TransactionMetricsResponseBucketedMetrics"
    group_by_columns: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aggregate_metrics = self.aggregate_metrics.to_dict()

        bucketed_metrics = self.bucketed_metrics.to_dict()

        group_by_columns = self.group_by_columns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "aggregate_metrics": aggregate_metrics,
                "bucketed_metrics": bucketed_metrics,
                "group_by_columns": group_by_columns,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aggregate_metrics import AggregateMetrics
        from ..models.transaction_metrics_response_bucketed_metrics import TransactionMetricsResponseBucketedMetrics

        d = src_dict.copy()
        aggregate_metrics = AggregateMetrics.from_dict(d.pop("aggregate_metrics"))

        bucketed_metrics = TransactionMetricsResponseBucketedMetrics.from_dict(d.pop("bucketed_metrics"))

        group_by_columns = cast(list[str], d.pop("group_by_columns"))

        transaction_metrics_response = cls(
            aggregate_metrics=aggregate_metrics, bucketed_metrics=bucketed_metrics, group_by_columns=group_by_columns
        )

        transaction_metrics_response.additional_properties = d
        return transaction_metrics_response

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
