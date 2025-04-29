from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExperimentUpdateRequest")


@_attrs_define
class ExperimentUpdateRequest:
    """
    Attributes:
        name (str):
        dataset_version_id (Union[None, Unset, str]):
        task_type (Union[Literal[16], Literal[17], Unset]):  Default: 16.
    """

    name: str
    dataset_version_id: Union[None, Unset, str] = UNSET
    task_type: Union[Literal[16], Literal[17], Unset] = 16
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        dataset_version_id: Union[None, Unset, str]
        if isinstance(self.dataset_version_id, Unset):
            dataset_version_id = UNSET
        else:
            dataset_version_id = self.dataset_version_id

        task_type: Union[Literal[16], Literal[17], Unset]
        if isinstance(self.task_type, Unset):
            task_type = UNSET
        else:
            task_type = self.task_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if dataset_version_id is not UNSET:
            field_dict["dataset_version_id"] = dataset_version_id
        if task_type is not UNSET:
            field_dict["task_type"] = task_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_dataset_version_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_version_id = _parse_dataset_version_id(d.pop("dataset_version_id", UNSET))

        def _parse_task_type(data: object) -> Union[Literal[16], Literal[17], Unset]:
            if isinstance(data, Unset):
                return data
            task_type_type_0 = cast(Literal[16], data)
            if task_type_type_0 != 16:
                raise ValueError(f"task_type_type_0 must match const 16, got '{task_type_type_0}'")
            return task_type_type_0
            task_type_type_1 = cast(Literal[17], data)
            if task_type_type_1 != 17:
                raise ValueError(f"task_type_type_1 must match const 17, got '{task_type_type_1}'")
            return task_type_type_1

        task_type = _parse_task_type(d.pop("task_type", UNSET))

        experiment_update_request = cls(name=name, dataset_version_id=dataset_version_id, task_type=task_type)

        experiment_update_request.additional_properties = d
        return experiment_update_request

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
