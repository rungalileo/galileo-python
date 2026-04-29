from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.invalid_result import InvalidResult
    from ..models.valid_result import ValidResult


T = TypeVar("T", bound="ValidateRegisteredScorerResult")


@_attrs_define
class ValidateRegisteredScorerResult:
    """
    Attributes
    ----------
        result (Union['InvalidResult', 'ValidResult']):
    """

    result: Union["InvalidResult", "ValidResult"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.valid_result import ValidResult

        result: dict[str, Any]
        result = self.result.to_dict() if isinstance(self.result, ValidResult) else self.result.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"result": result})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invalid_result import InvalidResult
        from ..models.valid_result import ValidResult

        d = dict(src_dict)

        def _parse_result(data: object) -> Union["InvalidResult", "ValidResult"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ValidResult.from_dict(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            return InvalidResult.from_dict(data)

        result = _parse_result(d.pop("result"))

        validate_registered_scorer_result = cls(result=result)

        validate_registered_scorer_result.additional_properties = d
        return validate_registered_scorer_result

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
