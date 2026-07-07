from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExperimentPhaseStatus")


@_attrs_define
class ExperimentPhaseStatus:
    """
    Attributes:
        progress_percent (Union[Unset, float]): Progress percentage from 0.0 to 1.0 Default: 0.0.
    """

    progress_percent: Union[Unset, float] = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        progress_percent = self.progress_percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if progress_percent is not UNSET:
            field_dict["progress_percent"] = progress_percent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        progress_percent = d.pop("progress_percent", UNSET)

        experiment_phase_status = cls(progress_percent=progress_percent)

        experiment_phase_status.additional_properties = d
        return experiment_phase_status

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
