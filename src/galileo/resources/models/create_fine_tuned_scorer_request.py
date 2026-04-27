from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.core_scorer_name import CoreScorerName
from ..models.luna_input_type_enum import LunaInputTypeEnum
from ..models.luna_output_type_enum import LunaOutputTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateFineTunedScorerRequest")


@_attrs_define
class CreateFineTunedScorerRequest:
    """
    Attributes:
        name (str):
        lora_task_id (int):
        prompt (str):
        lora_weights_path (None | str | Unset):
        executor (CoreScorerName | None | Unset): Executor pipeline. Defaults to finetuned scorer pipeline but can run
            custom galileo score pipelines.
        luna_input_type (LunaInputTypeEnum | None | Unset):
        luna_output_type (LunaOutputTypeEnum | None | Unset):
    """

    name: str
    lora_task_id: int
    prompt: str
    lora_weights_path: None | str | Unset = UNSET
    executor: CoreScorerName | None | Unset = UNSET
    luna_input_type: LunaInputTypeEnum | None | Unset = UNSET
    luna_output_type: LunaOutputTypeEnum | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        lora_task_id = self.lora_task_id

        prompt = self.prompt

        lora_weights_path: None | str | Unset
        if isinstance(self.lora_weights_path, Unset):
            lora_weights_path = UNSET
        else:
            lora_weights_path = self.lora_weights_path

        executor: None | str | Unset
        if isinstance(self.executor, Unset):
            executor = UNSET
        elif isinstance(self.executor, CoreScorerName):
            executor = self.executor.value
        else:
            executor = self.executor

        luna_input_type: None | str | Unset
        if isinstance(self.luna_input_type, Unset):
            luna_input_type = UNSET
        elif isinstance(self.luna_input_type, LunaInputTypeEnum):
            luna_input_type = self.luna_input_type.value
        else:
            luna_input_type = self.luna_input_type

        luna_output_type: None | str | Unset
        if isinstance(self.luna_output_type, Unset):
            luna_output_type = UNSET
        elif isinstance(self.luna_output_type, LunaOutputTypeEnum):
            luna_output_type = self.luna_output_type.value
        else:
            luna_output_type = self.luna_output_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "lora_task_id": lora_task_id, "prompt": prompt})
        if lora_weights_path is not UNSET:
            field_dict["lora_weights_path"] = lora_weights_path
        if executor is not UNSET:
            field_dict["executor"] = executor
        if luna_input_type is not UNSET:
            field_dict["luna_input_type"] = luna_input_type
        if luna_output_type is not UNSET:
            field_dict["luna_output_type"] = luna_output_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        lora_task_id = d.pop("lora_task_id")

        prompt = d.pop("prompt")

        def _parse_lora_weights_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        lora_weights_path = _parse_lora_weights_path(d.pop("lora_weights_path", UNSET))

        def _parse_executor(data: object) -> CoreScorerName | None | Unset:
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
            return cast(CoreScorerName | None | Unset, data)

        executor = _parse_executor(d.pop("executor", UNSET))

        def _parse_luna_input_type(data: object) -> LunaInputTypeEnum | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                luna_input_type_type_0 = LunaInputTypeEnum(data)

                return luna_input_type_type_0
            except:  # noqa: E722
                pass
            return cast(LunaInputTypeEnum | None | Unset, data)

        luna_input_type = _parse_luna_input_type(d.pop("luna_input_type", UNSET))

        def _parse_luna_output_type(data: object) -> LunaOutputTypeEnum | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                luna_output_type_type_0 = LunaOutputTypeEnum(data)

                return luna_output_type_type_0
            except:  # noqa: E722
                pass
            return cast(LunaOutputTypeEnum | None | Unset, data)

        luna_output_type = _parse_luna_output_type(d.pop("luna_output_type", UNSET))

        create_fine_tuned_scorer_request = cls(
            name=name,
            lora_task_id=lora_task_id,
            prompt=prompt,
            lora_weights_path=lora_weights_path,
            executor=executor,
            luna_input_type=luna_input_type,
            luna_output_type=luna_output_type,
        )

        create_fine_tuned_scorer_request.additional_properties = d
        return create_fine_tuned_scorer_request

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
