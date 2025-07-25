from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_type import ScorerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricNotComputed")


@_attrs_define
class MetricNotComputed:
    """
    Attributes:
        message (Union[Unset, str]):  Default: 'Metric not computed.'.
        scorer_type (Union[None, ScorerType, Unset]):
        status_type (Union[Literal['not_computed'], Unset]):  Default: 'not_computed'.
    """

    message: Union[Unset, str] = "Metric not computed."
    scorer_type: Union[None, ScorerType, Unset] = UNSET
    status_type: Union[Literal["not_computed"], Unset] = "not_computed"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        scorer_type: Union[None, Unset, str]
        if isinstance(self.scorer_type, Unset):
            scorer_type = UNSET
        elif isinstance(self.scorer_type, ScorerType):
            scorer_type = self.scorer_type.value
        else:
            scorer_type = self.scorer_type

        status_type = self.status_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if scorer_type is not UNSET:
            field_dict["scorer_type"] = scorer_type
        if status_type is not UNSET:
            field_dict["status_type"] = status_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message", UNSET)

        def _parse_scorer_type(data: object) -> Union[None, ScorerType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scorer_type_type_0 = ScorerType(data)

                return scorer_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ScorerType, Unset], data)

        scorer_type = _parse_scorer_type(d.pop("scorer_type", UNSET))

        status_type = cast(Union[Literal["not_computed"], Unset], d.pop("status_type", UNSET))
        if status_type != "not_computed" and not isinstance(status_type, Unset):
            raise ValueError(f"status_type must match const 'not_computed', got '{status_type}'")

        metric_not_computed = cls(message=message, scorer_type=scorer_type, status_type=status_type)

        metric_not_computed.additional_properties = d
        return metric_not_computed

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
