from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExperimentGroupIDFilter")


@_attrs_define
class ExperimentGroupIDFilter:
    """
    Attributes:
        value (str):
        name (Union[Literal['experiment_group_id'], Unset]):  Default: 'experiment_group_id'.
    """

    value: str
    name: Union[Literal["experiment_group_id"], Unset] = "experiment_group_id"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        name = cast(Union[Literal["experiment_group_id"], Unset], d.pop("name", UNSET))
        if name != "experiment_group_id" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'experiment_group_id', got '{name}'")

        experiment_group_id_filter = cls(value=value, name=name)

        experiment_group_id_filter.additional_properties = d
        return experiment_group_id_filter

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
