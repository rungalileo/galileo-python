import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.task_result_status import TaskResultStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.validate_registered_scorer_result import ValidateRegisteredScorerResult


T = TypeVar("T", bound="RegisteredScorerTaskResultResponse")


@_attrs_define
class RegisteredScorerTaskResultResponse:
    """
    Attributes
    ----------
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        status (TaskResultStatus):
        result (Union['ValidateRegisteredScorerResult', None, Unset, str]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: TaskResultStatus
    result: Union["ValidateRegisteredScorerResult", None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.validate_registered_scorer_result import ValidateRegisteredScorerResult

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        status = self.status.value

        result: Union[None, Unset, dict[str, Any], str]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, ValidateRegisteredScorerResult):
            result = self.result.to_dict()
        else:
            result = self.result

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "created_at": created_at, "updated_at": updated_at, "status": status})
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.validate_registered_scorer_result import ValidateRegisteredScorerResult

        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        status = TaskResultStatus(d.pop("status"))

        def _parse_result(data: object) -> Union["ValidateRegisteredScorerResult", None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ValidateRegisteredScorerResult.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ValidateRegisteredScorerResult", None, Unset, str], data)

        result = _parse_result(d.pop("result", UNSET))

        registered_scorer_task_result_response = cls(
            id=id, created_at=created_at, updated_at=updated_at, status=status, result=result
        )

        registered_scorer_task_result_response.additional_properties = d
        return registered_scorer_task_result_response

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
