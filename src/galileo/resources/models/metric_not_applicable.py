from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_type import ScorerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.standard_error import StandardError


T = TypeVar("T", bound="MetricNotApplicable")


@_attrs_define
class MetricNotApplicable:
    """
    Attributes
    ----------
        status_type (Union[Literal['not_applicable'], Unset]):  Default: 'not_applicable'.
        scorer_type (Union[None, ScorerType, Unset]):
        message (Union[Unset, str]):  Default: 'Metric not applicable.'.
        ems_error_code (Union[None, Unset, int]): EMS error code from errors.yaml catalog for this not-applicable reason
        standard_error (Union['StandardError', None, Unset]): Structured EMS error resolved on-the-fly from errors.yaml
            catalog.
    """

    status_type: Union[Literal["not_applicable"], Unset] = "not_applicable"
    scorer_type: Union[None, ScorerType, Unset] = UNSET
    message: Union[Unset, str] = "Metric not applicable."
    ems_error_code: Union[None, Unset, int] = UNSET
    standard_error: Union["StandardError", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.standard_error import StandardError

        status_type = self.status_type

        scorer_type: Union[None, Unset, str]
        if isinstance(self.scorer_type, Unset):
            scorer_type = UNSET
        elif isinstance(self.scorer_type, ScorerType):
            scorer_type = self.scorer_type.value
        else:
            scorer_type = self.scorer_type

        message = self.message

        ems_error_code: Union[None, Unset, int]
        ems_error_code = UNSET if isinstance(self.ems_error_code, Unset) else self.ems_error_code

        standard_error: Union[None, Unset, dict[str, Any]]
        if isinstance(self.standard_error, Unset):
            standard_error = UNSET
        elif isinstance(self.standard_error, StandardError):
            standard_error = self.standard_error.to_dict()
        else:
            standard_error = self.standard_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status_type is not UNSET:
            field_dict["status_type"] = status_type
        if scorer_type is not UNSET:
            field_dict["scorer_type"] = scorer_type
        if message is not UNSET:
            field_dict["message"] = message
        if ems_error_code is not UNSET:
            field_dict["ems_error_code"] = ems_error_code
        if standard_error is not UNSET:
            field_dict["standard_error"] = standard_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.standard_error import StandardError

        d = dict(src_dict)
        status_type = cast(Union[Literal["not_applicable"], Unset], d.pop("status_type", UNSET))
        if status_type != "not_applicable" and not isinstance(status_type, Unset):
            raise ValueError(f"status_type must match const 'not_applicable', got '{status_type}'")

        def _parse_scorer_type(data: object) -> Union[None, ScorerType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ScorerType(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, ScorerType, Unset], data)

        scorer_type = _parse_scorer_type(d.pop("scorer_type", UNSET))

        message = d.pop("message", UNSET)

        def _parse_ems_error_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        ems_error_code = _parse_ems_error_code(d.pop("ems_error_code", UNSET))

        def _parse_standard_error(data: object) -> Union["StandardError", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return StandardError.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["StandardError", None, Unset], data)

        standard_error = _parse_standard_error(d.pop("standard_error", UNSET))

        metric_not_applicable = cls(
            status_type=status_type,
            scorer_type=scorer_type,
            message=message,
            ems_error_code=ems_error_code,
            standard_error=standard_error,
        )

        metric_not_applicable.additional_properties = d
        return metric_not_applicable

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
