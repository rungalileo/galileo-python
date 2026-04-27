from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.generated_scorer_task_result_type import GeneratedScorerTaskResultType
from ..models.task_result_status import TaskResultStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.generated_scorer_validation_result import GeneratedScorerValidationResult


T = TypeVar("T", bound="GeneratedScorerTaskResultResponse")


@_attrs_define
class GeneratedScorerTaskResultResponse:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        status (TaskResultStatus):
        result_type (GeneratedScorerTaskResultType):
        result (ChainPollTemplate | GeneratedScorerValidationResult | None | str | Unset):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: TaskResultStatus
    result_type: GeneratedScorerTaskResultType
    result: ChainPollTemplate | GeneratedScorerValidationResult | None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.generated_scorer_validation_result import GeneratedScorerValidationResult

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        status = self.status.value

        result_type = self.result_type.value

        result: dict[str, Any] | None | str | Unset
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, ChainPollTemplate):
            result = self.result.to_dict()
        elif isinstance(self.result, GeneratedScorerValidationResult):
            result = self.result.to_dict()
        else:
            result = self.result

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "created_at": created_at, "updated_at": updated_at, "status": status, "result_type": result_type}
        )
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.generated_scorer_validation_result import GeneratedScorerValidationResult

        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        status = TaskResultStatus(d.pop("status"))

        result_type = GeneratedScorerTaskResultType(d.pop("result_type"))

        def _parse_result(data: object) -> ChainPollTemplate | GeneratedScorerValidationResult | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = ChainPollTemplate.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_1 = GeneratedScorerValidationResult.from_dict(data)

                return result_type_1
            except:  # noqa: E722
                pass
            return cast(ChainPollTemplate | GeneratedScorerValidationResult | None | str | Unset, data)

        result = _parse_result(d.pop("result", UNSET))

        generated_scorer_task_result_response = cls(
            id=id, created_at=created_at, updated_at=updated_at, status=status, result_type=result_type, result=result
        )

        generated_scorer_task_result_response.additional_properties = d
        return generated_scorer_task_result_response

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
