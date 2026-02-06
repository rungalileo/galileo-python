from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.core_scorer_name import CoreScorerName
from ..models.luna_input_type_enum import LunaInputTypeEnum
from ..models.luna_output_type_enum import LunaOutputTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCustomLunaScorerVersionRequest")


@_attrs_define
class CreateCustomLunaScorerVersionRequest:
    """
    Attributes
    ----------
        lora_task_id (int):
        prompt (str):
        lora_weights_path (Union[None, Unset, str]):
        executor (Union[CoreScorerName, None, Unset]): Executor pipeline. Defaults to finetuned scorer pipeline but can
            run custom galileo score pipelines.
        luna_input_type (Union[LunaInputTypeEnum, None, Unset]):
        luna_output_type (Union[LunaOutputTypeEnum, None, Unset]):
    """

    lora_task_id: int
    prompt: str
    lora_weights_path: Union[None, Unset, str] = UNSET
    executor: Union[CoreScorerName, None, Unset] = UNSET
    luna_input_type: Union[LunaInputTypeEnum, None, Unset] = UNSET
    luna_output_type: Union[LunaOutputTypeEnum, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lora_task_id = self.lora_task_id

        prompt = self.prompt

        lora_weights_path: Union[None, Unset, str]
        lora_weights_path = UNSET if isinstance(self.lora_weights_path, Unset) else self.lora_weights_path

        executor: Union[None, Unset, str]
        if isinstance(self.executor, Unset):
            executor = UNSET
        elif isinstance(self.executor, CoreScorerName):
            executor = self.executor.value
        else:
            executor = self.executor

        luna_input_type: Union[None, Unset, str]
        if isinstance(self.luna_input_type, Unset):
            luna_input_type = UNSET
        elif isinstance(self.luna_input_type, LunaInputTypeEnum):
            luna_input_type = self.luna_input_type.value
        else:
            luna_input_type = self.luna_input_type

        luna_output_type: Union[None, Unset, str]
        if isinstance(self.luna_output_type, Unset):
            luna_output_type = UNSET
        elif isinstance(self.luna_output_type, LunaOutputTypeEnum):
            luna_output_type = self.luna_output_type.value
        else:
            luna_output_type = self.luna_output_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"lora_task_id": lora_task_id, "prompt": prompt})
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
        lora_task_id = d.pop("lora_task_id")

        prompt = d.pop("prompt")

        def _parse_lora_weights_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        lora_weights_path = _parse_lora_weights_path(d.pop("lora_weights_path", UNSET))

        def _parse_executor(data: object) -> Union[CoreScorerName, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return CoreScorerName(data)

            except:  # noqa: E722
                pass
            return cast(Union[CoreScorerName, None, Unset], data)

        executor = _parse_executor(d.pop("executor", UNSET))

        def _parse_luna_input_type(data: object) -> Union[LunaInputTypeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return LunaInputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(Union[LunaInputTypeEnum, None, Unset], data)

        luna_input_type = _parse_luna_input_type(d.pop("luna_input_type", UNSET))

        def _parse_luna_output_type(data: object) -> Union[LunaOutputTypeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return LunaOutputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(Union[LunaOutputTypeEnum, None, Unset], data)

        luna_output_type = _parse_luna_output_type(d.pop("luna_output_type", UNSET))

        create_custom_luna_scorer_version_request = cls(
            lora_task_id=lora_task_id,
            prompt=prompt,
            lora_weights_path=lora_weights_path,
            executor=executor,
            luna_input_type=luna_input_type,
            luna_output_type=luna_output_type,
        )

        create_custom_luna_scorer_version_request.additional_properties = d
        return create_custom_luna_scorer_version_request

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
