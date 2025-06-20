from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecomputeSettingsLogStream")


@_attrs_define
class RecomputeSettingsLogStream:
    """
    Attributes:
        filters (list[Any]):
        run_id (str):
        mode (Union[Literal['log_stream_filters'], Unset]):  Default: 'log_stream_filters'.
    """

    filters: list[Any]
    run_id: str
    mode: Union[Literal["log_stream_filters"], Unset] = "log_stream_filters"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters = self.filters

        run_id = self.run_id

        mode = self.mode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"filters": filters, "run_id": run_id})
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filters = cast(list[Any], d.pop("filters"))

        run_id = d.pop("run_id")

        mode = cast(Union[Literal["log_stream_filters"], Unset], d.pop("mode", UNSET))
        if mode != "log_stream_filters" and not isinstance(mode, Unset):
            raise ValueError(f"mode must match const 'log_stream_filters', got '{mode}'")

        recompute_settings_log_stream = cls(filters=filters, run_id=run_id, mode=mode)

        recompute_settings_log_stream.additional_properties = d
        return recompute_settings_log_stream

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
