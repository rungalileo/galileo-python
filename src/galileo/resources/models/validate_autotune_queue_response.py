from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ValidateAutotuneQueueResponse")


@_attrs_define
class ValidateAutotuneQueueResponse:
    """Response for autotune queue validation (202 Accepted).

    Attributes:
        metrics_testing_run_id (str): ID of the metrics testing run containing validation results
        project_id (str): Project where the metrics testing run was created
        queue_id (str): Queue ID that was tested
        feedback_count (int): Number of feedback records tested
    """

    metrics_testing_run_id: str
    project_id: str
    queue_id: str
    feedback_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metrics_testing_run_id = self.metrics_testing_run_id

        project_id = self.project_id

        queue_id = self.queue_id

        feedback_count = self.feedback_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metrics_testing_run_id": metrics_testing_run_id,
                "project_id": project_id,
                "queue_id": queue_id,
                "feedback_count": feedback_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metrics_testing_run_id = d.pop("metrics_testing_run_id")

        project_id = d.pop("project_id")

        queue_id = d.pop("queue_id")

        feedback_count = d.pop("feedback_count")

        validate_autotune_queue_response = cls(
            metrics_testing_run_id=metrics_testing_run_id,
            project_id=project_id,
            queue_id=queue_id,
            feedback_count=feedback_count,
        )

        validate_autotune_queue_response.additional_properties = d
        return validate_autotune_queue_response

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
