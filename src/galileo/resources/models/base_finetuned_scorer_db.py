from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.core_scorer_name import CoreScorerName
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseFinetunedScorerDB")


@_attrs_define
class BaseFinetunedScorerDB:
    """
    Attributes:
        id (str):
        lora_task_id (int):
        name (str):
        prompt (str):
        executor (Union[CoreScorerName, None, Unset]): Executor pipeline. Defaults to finetuned scorer pipeline but can
            run custom galileo score pipelines.
    """

    id: str
    lora_task_id: int
    name: str
    prompt: str
    executor: Union[CoreScorerName, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        lora_task_id = self.lora_task_id

        name = self.name

        prompt = self.prompt

        executor: Union[None, Unset, str]
        if isinstance(self.executor, Unset):
            executor = UNSET
        elif isinstance(self.executor, CoreScorerName):
            executor = self.executor.value
        else:
            executor = self.executor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "lora_task_id": lora_task_id, "name": name, "prompt": prompt})
        if executor is not UNSET:
            field_dict["executor"] = executor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        lora_task_id = d.pop("lora_task_id")

        name = d.pop("name")

        prompt = d.pop("prompt")

        def _parse_executor(data: object) -> Union[CoreScorerName, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                executor_type_0 = CoreScorerName(data)

                return executor_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CoreScorerName, None, Unset], data)

        executor = _parse_executor(d.pop("executor", UNSET))

        base_finetuned_scorer_db = cls(id=id, lora_task_id=lora_task_id, name=name, prompt=prompt, executor=executor)

        base_finetuned_scorer_db.additional_properties = d
        return base_finetuned_scorer_db

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
