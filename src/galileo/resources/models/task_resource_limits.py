from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskResourceLimits")


@_attrs_define
class TaskResourceLimits:
    """
    Attributes:
        cpu_time (Union[Unset, int]):  Default: 216.
        memory_mb (Union[Unset, int]):  Default: 160.
    """

    cpu_time: Union[Unset, int] = 216
    memory_mb: Union[Unset, int] = 160
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_time = self.cpu_time

        memory_mb = self.memory_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu_time is not UNSET:
            field_dict["cpu_time"] = cpu_time
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cpu_time = d.pop("cpu_time", UNSET)

        memory_mb = d.pop("memory_mb", UNSET)

        task_resource_limits = cls(cpu_time=cpu_time, memory_mb=memory_mb)

        task_resource_limits.additional_properties = d
        return task_resource_limits

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
