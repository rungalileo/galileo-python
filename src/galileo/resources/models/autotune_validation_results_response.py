from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.autotune_validation_status import AutotuneValidationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.autotune_validation_result_item import AutotuneValidationResultItem


T = TypeVar("T", bound="AutotuneValidationResultsResponse")


@_attrs_define
class AutotuneValidationResultsResponse:
    """Response for the autotune validation results endpoint (pollable).

    Attributes:
        queue_id (str): Queue ID
        status (AutotuneValidationStatus): Status of autotune validation scoring.
        total_count (int): Total number of feedback items
        scored_count (int): Number of feedback items that have been scored
        metrics_testing_run_id (None | str | Unset): Metrics testing run ID, null if validation not started
        results (list[AutotuneValidationResultItem] | Unset): One row per feedback item
    """

    queue_id: str
    status: AutotuneValidationStatus
    total_count: int
    scored_count: int
    metrics_testing_run_id: None | str | Unset = UNSET
    results: list[AutotuneValidationResultItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        queue_id = self.queue_id

        status = self.status.value

        total_count = self.total_count

        scored_count = self.scored_count

        metrics_testing_run_id: None | str | Unset
        if isinstance(self.metrics_testing_run_id, Unset):
            metrics_testing_run_id = UNSET
        else:
            metrics_testing_run_id = self.metrics_testing_run_id

        results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"queue_id": queue_id, "status": status, "total_count": total_count, "scored_count": scored_count}
        )
        if metrics_testing_run_id is not UNSET:
            field_dict["metrics_testing_run_id"] = metrics_testing_run_id
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autotune_validation_result_item import AutotuneValidationResultItem

        d = dict(src_dict)
        queue_id = d.pop("queue_id")

        status = AutotuneValidationStatus(d.pop("status"))

        total_count = d.pop("total_count")

        scored_count = d.pop("scored_count")

        def _parse_metrics_testing_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metrics_testing_run_id = _parse_metrics_testing_run_id(d.pop("metrics_testing_run_id", UNSET))

        _results = d.pop("results", UNSET)
        results: list[AutotuneValidationResultItem] | Unset = UNSET
        if _results is not UNSET:
            results = []
            for results_item_data in _results:
                results_item = AutotuneValidationResultItem.from_dict(results_item_data)

                results.append(results_item)

        autotune_validation_results_response = cls(
            queue_id=queue_id,
            status=status,
            total_count=total_count,
            scored_count=scored_count,
            metrics_testing_run_id=metrics_testing_run_id,
            results=results,
        )

        autotune_validation_results_response.additional_properties = d
        return autotune_validation_results_response

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
