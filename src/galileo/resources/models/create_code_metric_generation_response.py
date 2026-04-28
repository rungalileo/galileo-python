from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.code_metric_generation_status import CodeMetricGenerationStatus

T = TypeVar("T", bound="CreateCodeMetricGenerationResponse")


@_attrs_define
class CreateCodeMetricGenerationResponse:
    """Response with generation ID for polling.

    Attributes
    ----------
        id (str):
        status (CodeMetricGenerationStatus):
    """

    id: str
    status: CodeMetricGenerationStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "status": status})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = CodeMetricGenerationStatus(d.pop("status"))

        create_code_metric_generation_response = cls(id=id, status=status)

        create_code_metric_generation_response.additional_properties = d
        return create_code_metric_generation_response

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
