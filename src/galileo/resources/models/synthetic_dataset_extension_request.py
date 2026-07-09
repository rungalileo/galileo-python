from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.synthetic_data_types import SyntheticDataTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prompt_run_settings import PromptRunSettings
    from ..models.synthetic_data_source_dataset import SyntheticDataSourceDataset


T = TypeVar("T", bound="SyntheticDatasetExtensionRequest")


@_attrs_define
class SyntheticDatasetExtensionRequest:
    """Request for a synthetic dataset run job.

    Attributes:
        prompt_settings (PromptRunSettings | Unset): Prompt run settings.
        prompt (None | str | Unset):
        instructions (None | str | Unset):
        examples (list[str] | Unset):
        source_dataset (None | SyntheticDataSourceDataset | Unset):
        data_types (list[SyntheticDataTypes] | None | Unset):
        count (int | Unset):  Default: 10.
        project_id (None | str | Unset):
    """

    prompt_settings: PromptRunSettings | Unset = UNSET
    prompt: None | str | Unset = UNSET
    instructions: None | str | Unset = UNSET
    examples: list[str] | Unset = UNSET
    source_dataset: None | SyntheticDataSourceDataset | Unset = UNSET
    data_types: list[SyntheticDataTypes] | None | Unset = UNSET
    count: int | Unset = 10
    project_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.synthetic_data_source_dataset import SyntheticDataSourceDataset

        prompt_settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.prompt_settings, Unset):
            prompt_settings = self.prompt_settings.to_dict()

        prompt: None | str | Unset
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        instructions: None | str | Unset
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        examples: list[str] | Unset = UNSET
        if not isinstance(self.examples, Unset):
            examples = self.examples

        source_dataset: dict[str, Any] | None | Unset
        if isinstance(self.source_dataset, Unset):
            source_dataset = UNSET
        elif isinstance(self.source_dataset, SyntheticDataSourceDataset):
            source_dataset = self.source_dataset.to_dict()
        else:
            source_dataset = self.source_dataset

        data_types: list[str] | None | Unset
        if isinstance(self.data_types, Unset):
            data_types = UNSET
        elif isinstance(self.data_types, list):
            data_types = []
            for data_types_type_0_item_data in self.data_types:
                data_types_type_0_item = data_types_type_0_item_data.value
                data_types.append(data_types_type_0_item)

        else:
            data_types = self.data_types

        count = self.count

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prompt_settings is not UNSET:
            field_dict["prompt_settings"] = prompt_settings
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if examples is not UNSET:
            field_dict["examples"] = examples
        if source_dataset is not UNSET:
            field_dict["source_dataset"] = source_dataset
        if data_types is not UNSET:
            field_dict["data_types"] = data_types
        if count is not UNSET:
            field_dict["count"] = count
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.synthetic_data_source_dataset import SyntheticDataSourceDataset

        d = dict(src_dict)
        _prompt_settings = d.pop("prompt_settings", UNSET)
        prompt_settings: PromptRunSettings | Unset
        if isinstance(_prompt_settings, Unset):
            prompt_settings = UNSET
        else:
            prompt_settings = PromptRunSettings.from_dict(_prompt_settings)

        def _parse_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        def _parse_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        examples = cast(list[str], d.pop("examples", UNSET))

        def _parse_source_dataset(data: object) -> None | SyntheticDataSourceDataset | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_dataset_type_0 = SyntheticDataSourceDataset.from_dict(data)

                return source_dataset_type_0
            except:  # noqa: E722
                pass
            return cast(None | SyntheticDataSourceDataset | Unset, data)

        source_dataset = _parse_source_dataset(d.pop("source_dataset", UNSET))

        def _parse_data_types(data: object) -> list[SyntheticDataTypes] | None | Unset:
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
            return cast(list[SyntheticDataTypes] | None | Unset, data)

        data_types = _parse_data_types(d.pop("data_types", UNSET))

        count = d.pop("count", UNSET)

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        synthetic_dataset_extension_request = cls(
            prompt_settings=prompt_settings,
            prompt=prompt,
            instructions=instructions,
            examples=examples,
            source_dataset=source_dataset,
            data_types=data_types,
            count=count,
            project_id=project_id,
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
