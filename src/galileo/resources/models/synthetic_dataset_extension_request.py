from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.synthetic_data_types import SyntheticDataTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prompt_run_settings import PromptRunSettings


T = TypeVar("T", bound="SyntheticDatasetExtensionRequest")


@_attrs_define
class SyntheticDatasetExtensionRequest:
    """Request for a synthetic dataset run job.

    Attributes:
        count (Union[Unset, int]):  Default: 10.
        data_types (Union[None, Unset, list[SyntheticDataTypes]]):
        examples (Union[None, Unset, list[str]]):
        instructions (Union[None, Unset, str]):
        prompt (Union[None, Unset, str]):
        prompt_settings (Union[Unset, PromptRunSettings]): Prompt run settings.
    """

    count: Union[Unset, int] = 10
    data_types: Union[None, Unset, list[SyntheticDataTypes]] = UNSET
    examples: Union[None, Unset, list[str]] = UNSET
    instructions: Union[None, Unset, str] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    prompt_settings: Union[Unset, "PromptRunSettings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        data_types: Union[None, Unset, list[str]]
        if isinstance(self.data_types, Unset):
            data_types = UNSET
        elif isinstance(self.data_types, list):
            data_types = []
            for data_types_type_0_item_data in self.data_types:
                data_types_type_0_item = data_types_type_0_item_data.value
                data_types.append(data_types_type_0_item)

        else:
            data_types = self.data_types

        examples: Union[None, Unset, list[str]]
        if isinstance(self.examples, Unset):
            examples = UNSET
        elif isinstance(self.examples, list):
            examples = self.examples

        else:
            examples = self.examples

        instructions: Union[None, Unset, str]
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        prompt: Union[None, Unset, str]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        prompt_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.prompt_settings, Unset):
            prompt_settings = self.prompt_settings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if data_types is not UNSET:
            field_dict["data_types"] = data_types
        if examples is not UNSET:
            field_dict["examples"] = examples
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if prompt_settings is not UNSET:
            field_dict["prompt_settings"] = prompt_settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prompt_run_settings import PromptRunSettings

        d = dict(src_dict)
        count = d.pop("count", UNSET)

        def _parse_data_types(data: object) -> Union[None, Unset, list[SyntheticDataTypes]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                data_types_type_0 = []
                _data_types_type_0 = data
                for data_types_type_0_item_data in _data_types_type_0:
                    data_types_type_0_item = SyntheticDataTypes(data_types_type_0_item_data)

                    data_types_type_0.append(data_types_type_0_item)

                return data_types_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[SyntheticDataTypes]], data)

        data_types = _parse_data_types(d.pop("data_types", UNSET))

        def _parse_examples(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                examples_type_0 = cast(list[str], data)

                return examples_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        examples = _parse_examples(d.pop("examples", UNSET))

        def _parse_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        _prompt_settings = d.pop("prompt_settings", UNSET)
        prompt_settings: Union[Unset, PromptRunSettings]
        if isinstance(_prompt_settings, Unset):
            prompt_settings = UNSET
        else:
            prompt_settings = PromptRunSettings.from_dict(_prompt_settings)

        synthetic_dataset_extension_request = cls(
            count=count,
            data_types=data_types,
            examples=examples,
            instructions=instructions,
            prompt=prompt,
            prompt_settings=prompt_settings,
        )

        synthetic_dataset_extension_request.additional_properties = d
        return synthetic_dataset_extension_request

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
