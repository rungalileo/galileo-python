from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_dataset_request import ExperimentDatasetRequest


T = TypeVar("T", bound="ExperimentCreateRequest")


@_attrs_define
class ExperimentCreateRequest:
    """
    Attributes:
        name (str):
        dataset (Union['ExperimentDatasetRequest', None, Unset]):
        playground_id (Union[None, Unset, str]):
        playground_prompt_id (Union[None, Unset, str]):
        task_type (Union[Literal[16], Literal[17], Unset]):  Default: 16.
    """

    name: str
    dataset: Union["ExperimentDatasetRequest", None, Unset] = UNSET
    playground_id: Union[None, Unset, str] = UNSET
    playground_prompt_id: Union[None, Unset, str] = UNSET
    task_type: Union[Literal[16], Literal[17], Unset] = 16
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.experiment_dataset_request import ExperimentDatasetRequest

        name = self.name

        dataset: Union[None, Unset, dict[str, Any]]
        if isinstance(self.dataset, Unset):
            dataset = UNSET
        elif isinstance(self.dataset, ExperimentDatasetRequest):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        playground_id: Union[None, Unset, str]
        if isinstance(self.playground_id, Unset):
            playground_id = UNSET
        else:
            playground_id = self.playground_id

        playground_prompt_id: Union[None, Unset, str]
        if isinstance(self.playground_prompt_id, Unset):
            playground_prompt_id = UNSET
        else:
            playground_prompt_id = self.playground_prompt_id

        task_type: Union[Literal[16], Literal[17], Unset]
        if isinstance(self.task_type, Unset):
            task_type = UNSET
        else:
            task_type = self.task_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if playground_id is not UNSET:
            field_dict["playground_id"] = playground_id
        if playground_prompt_id is not UNSET:
            field_dict["playground_prompt_id"] = playground_prompt_id
        if task_type is not UNSET:
            field_dict["task_type"] = task_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.experiment_dataset_request import ExperimentDatasetRequest

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_dataset(data: object) -> Union["ExperimentDatasetRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_type_0 = ExperimentDatasetRequest.from_dict(data)

                return dataset_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ExperimentDatasetRequest", None, Unset], data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        def _parse_playground_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        playground_id = _parse_playground_id(d.pop("playground_id", UNSET))

        def _parse_playground_prompt_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        playground_prompt_id = _parse_playground_prompt_id(d.pop("playground_prompt_id", UNSET))

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

        experiment_create_request = cls(
            name=name,
            dataset=dataset,
            playground_id=playground_id,
            playground_prompt_id=playground_prompt_id,
            task_type=task_type,
        )

        experiment_create_request.additional_properties = d
        return experiment_create_request

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
