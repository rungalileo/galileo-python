from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_phase_status import ExperimentPhaseStatus


T = TypeVar("T", bound="ExperimentStatus")


@_attrs_define
class ExperimentStatus:
    """
    Attributes:
        log_generation (Union[Unset, ExperimentPhaseStatus]):
    """

    log_generation: Union[Unset, "ExperimentPhaseStatus"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        log_generation: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.log_generation, Unset):
            log_generation = self.log_generation.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if log_generation is not UNSET:
            field_dict["log_generation"] = log_generation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.experiment_phase_status import ExperimentPhaseStatus

        d = dict(src_dict)
        _log_generation = d.pop("log_generation", UNSET)
        log_generation: Union[Unset, ExperimentPhaseStatus]
        if isinstance(_log_generation, Unset):
            log_generation = UNSET
        else:
            log_generation = ExperimentPhaseStatus.from_dict(_log_generation)

        experiment_status = cls(log_generation=log_generation)

        experiment_status.additional_properties = d
        return experiment_status

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
