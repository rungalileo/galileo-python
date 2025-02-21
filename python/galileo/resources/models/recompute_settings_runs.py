from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecomputeSettingsRuns")


@_attrs_define
class RecomputeSettingsRuns:
    """
    Attributes:
        run_ids (list[str]):
        mode (Union[Literal['runs'], Unset]):  Default: 'runs'.
    """

    run_ids: list[str]
    mode: Union[Literal["runs"], Unset] = "runs"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        run_ids = self.run_ids

        mode = self.mode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"run_ids": run_ids})
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        run_ids = cast(list[str], d.pop("run_ids"))

        mode = cast(Union[Literal["runs"], Unset], d.pop("mode", UNSET))
        if mode != "runs" and not isinstance(mode, Unset):
            raise ValueError(f"mode must match const 'runs', got '{mode}'")

        recompute_settings_runs = cls(run_ids=run_ids, mode=mode)

        recompute_settings_runs.additional_properties = d
        return recompute_settings_runs

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
