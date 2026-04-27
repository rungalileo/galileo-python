from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_modality import ContentModality
from ..models.llm_integration import LLMIntegration
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelInfo")


@_attrs_define
class ModelInfo:
    """Model information that is useful to surface to the UI and in other contexts.

    This is a subset of all of the information we store about the model. We need a lot more
    information to actually execute requests against the model, but that is not necessary
    to surface to the user.

        Attributes:
            name (str):
            alias (str):
            integration (LLMIntegration | Unset):
            user_role (None | str | Unset):
            assistant_role (None | str | Unset):
            system_supported (bool | Unset):  Default: False.
            input_modalities (list[ContentModality] | Unset): Input modalities that the model can accept.
    """

    name: str
    alias: str
    integration: LLMIntegration | Unset = UNSET
    user_role: None | str | Unset = UNSET
    assistant_role: None | str | Unset = UNSET
    system_supported: bool | Unset = False
    input_modalities: list[ContentModality] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        alias = self.alias

        integration: str | Unset = UNSET
        if not isinstance(self.integration, Unset):
            integration = self.integration.value

        user_role: None | str | Unset
        if isinstance(self.user_role, Unset):
            user_role = UNSET
        else:
            user_role = self.user_role

        assistant_role: None | str | Unset
        if isinstance(self.assistant_role, Unset):
            assistant_role = UNSET
        else:
            assistant_role = self.assistant_role

        system_supported = self.system_supported

        input_modalities: list[str] | Unset = UNSET
        if not isinstance(self.input_modalities, Unset):
            input_modalities = []
            for input_modalities_item_data in self.input_modalities:
                input_modalities_item = input_modalities_item_data.value
                input_modalities.append(input_modalities_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "alias": alias})
        if integration is not UNSET:
            field_dict["integration"] = integration
        if user_role is not UNSET:
            field_dict["user_role"] = user_role
        if assistant_role is not UNSET:
            field_dict["assistant_role"] = assistant_role
        if system_supported is not UNSET:
            field_dict["system_supported"] = system_supported
        if input_modalities is not UNSET:
            field_dict["input_modalities"] = input_modalities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        alias = d.pop("alias")

        _integration = d.pop("integration", UNSET)
        integration: LLMIntegration | Unset
        if isinstance(_integration, Unset):
            integration = UNSET
        else:
            integration = LLMIntegration(_integration)

        def _parse_user_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_role = _parse_user_role(d.pop("user_role", UNSET))

        def _parse_assistant_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        assistant_role = _parse_assistant_role(d.pop("assistant_role", UNSET))

        system_supported = d.pop("system_supported", UNSET)

        _input_modalities = d.pop("input_modalities", UNSET)
        input_modalities: list[ContentModality] | Unset = UNSET
        if _input_modalities is not UNSET:
            input_modalities = []
            for input_modalities_item_data in _input_modalities:
                input_modalities_item = ContentModality(input_modalities_item_data)

                input_modalities.append(input_modalities_item)

        model_info = cls(
            name=name,
            alias=alias,
            integration=integration,
            user_role=user_role,
            assistant_role=assistant_role,
            system_supported=system_supported,
            input_modalities=input_modalities,
        )

        model_info.additional_properties = d
        return model_info

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
