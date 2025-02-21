import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.generated_scorer_task_result_status import GeneratedScorerTaskResultStatus
from ..models.generated_scorer_task_result_type import GeneratedScorerTaskResultType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.auto_gen_result import AutoGenResult
    from ..models.generated_scorer_validation_result import GeneratedScorerValidationResult


T = TypeVar("T", bound="GeneratedScorerTaskResultResponse")


@_attrs_define
class GeneratedScorerTaskResultResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        result_type (GeneratedScorerTaskResultType):
        status (GeneratedScorerTaskResultStatus):
        updated_at (datetime.datetime):
        result (Union['AutoGenResult', 'GeneratedScorerValidationResult', None, Unset, str]):
    """

    created_at: datetime.datetime
    id: str
    result_type: GeneratedScorerTaskResultType
    status: GeneratedScorerTaskResultStatus
    updated_at: datetime.datetime
    result: Union["AutoGenResult", "GeneratedScorerValidationResult", None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.auto_gen_result import AutoGenResult
        from ..models.generated_scorer_validation_result import GeneratedScorerValidationResult

        created_at = self.created_at.isoformat()

        id = self.id

        result_type = self.result_type.value

        status = self.status.value

        updated_at = self.updated_at.isoformat()

        result: Union[None, Unset, dict[str, Any], str]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, AutoGenResult):
            result = self.result.to_dict()
        elif isinstance(self.result, GeneratedScorerValidationResult):
            result = self.result.to_dict()
        else:
            result = self.result

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"created_at": created_at, "id": id, "result_type": result_type, "status": status, "updated_at": updated_at}
        )
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.auto_gen_result import AutoGenResult
        from ..models.generated_scorer_validation_result import GeneratedScorerValidationResult

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        id = d.pop("id")

        result_type = GeneratedScorerTaskResultType(d.pop("result_type"))

        status = GeneratedScorerTaskResultStatus(d.pop("status"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_result(data: object) -> Union["AutoGenResult", "GeneratedScorerValidationResult", None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = AutoGenResult.from_dict(data)

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
            return cast(Union["AutoGenResult", "GeneratedScorerValidationResult", None, Unset, str], data)

        result = _parse_result(d.pop("result", UNSET))

        generated_scorer_task_result_response = cls(
            created_at=created_at, id=id, result_type=result_type, status=status, updated_at=updated_at, result=result
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
