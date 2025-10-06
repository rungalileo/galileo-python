from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExperimentPrompt")


@_attrs_define
class ExperimentPrompt:
    """
    Attributes:
        content (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        prompt_template_id (Union[None, Unset, str]):
        version_index (Union[None, Unset, int]):
    """

    content: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    prompt_template_id: Union[None, Unset, str] = UNSET
    version_index: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content: Union[None, Unset, str]
        content = UNSET if isinstance(self.content, Unset) else self.content

        name: Union[None, Unset, str]
        name = UNSET if isinstance(self.name, Unset) else self.name

        prompt_template_id: Union[None, Unset, str]
        prompt_template_id = UNSET if isinstance(self.prompt_template_id, Unset) else self.prompt_template_id

        version_index: Union[None, Unset, int]
        version_index = UNSET if isinstance(self.version_index, Unset) else self.version_index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if name is not UNSET:
            field_dict["name"] = name
        if prompt_template_id is not UNSET:
            field_dict["prompt_template_id"] = prompt_template_id
        if version_index is not UNSET:
            field_dict["version_index"] = version_index

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_content(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content = _parse_content(d.pop("content", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_prompt_template_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt_template_id = _parse_prompt_template_id(d.pop("prompt_template_id", UNSET))

        def _parse_version_index(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        version_index = _parse_version_index(d.pop("version_index", UNSET))

        experiment_prompt = cls(
            content=content, name=name, prompt_template_id=prompt_template_id, version_index=version_index
        )

        experiment_prompt.additional_properties = d
        return experiment_prompt

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
