from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.code_metric_generation_status import CodeMetricGenerationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CodeMetricGenerationStatusResponse")


@_attrs_define
class CodeMetricGenerationStatusResponse:
    """Lightweight polling response.

    Attributes
    ----------
        id (str):
        status (CodeMetricGenerationStatus):
        generated_code (None | str | Unset):
        error_message (None | str | Unset):
    """

    id: str
    status: CodeMetricGenerationStatus
    generated_code: None | str | Unset = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        generated_code: None | str | Unset
        generated_code = UNSET if isinstance(self.generated_code, Unset) else self.generated_code

        error_message: None | str | Unset
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "status": status})
        if generated_code is not UNSET:
            field_dict["generated_code"] = generated_code
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = CodeMetricGenerationStatus(d.pop("status"))

        def _parse_generated_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        generated_code = _parse_generated_code(d.pop("generated_code", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        code_metric_generation_status_response = cls(
            id=id, status=status, generated_code=generated_code, error_message=error_message
        )

        code_metric_generation_status_response.additional_properties = d
        return code_metric_generation_status_response

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
