from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
            alias (str):
            name (str):
            assistant_role (Union[None, Unset, str]):
            integration (Union[Unset, LLMIntegration]):
            system_supported (Union[Unset, bool]):  Default: False.
            user_role (Union[None, Unset, str]):
    """

    alias: str
    name: str
    assistant_role: Union[None, Unset, str] = UNSET
    integration: Union[Unset, LLMIntegration] = UNSET
    system_supported: Union[Unset, bool] = False
    user_role: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alias = self.alias

        name = self.name

        assistant_role: Union[None, Unset, str]
        if isinstance(self.assistant_role, Unset):
            assistant_role = UNSET
        else:
            assistant_role = self.assistant_role

        integration: Union[Unset, str] = UNSET
        if not isinstance(self.integration, Unset):
            integration = self.integration.value

        system_supported = self.system_supported

        user_role: Union[None, Unset, str]
        if isinstance(self.user_role, Unset):
            user_role = UNSET
        else:
            user_role = self.user_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"alias": alias, "name": name})
        if assistant_role is not UNSET:
            field_dict["assistant_role"] = assistant_role
        if integration is not UNSET:
            field_dict["integration"] = integration
        if system_supported is not UNSET:
            field_dict["system_supported"] = system_supported
        if user_role is not UNSET:
            field_dict["user_role"] = user_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        alias = d.pop("alias")

        name = d.pop("name")

        def _parse_assistant_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        assistant_role = _parse_assistant_role(d.pop("assistant_role", UNSET))

        _integration = d.pop("integration", UNSET)
        integration: Union[Unset, LLMIntegration]
        if isinstance(_integration, Unset):
            integration = UNSET
        else:
            integration = LLMIntegration(_integration)

        system_supported = d.pop("system_supported", UNSET)

        def _parse_user_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_role = _parse_user_role(d.pop("user_role", UNSET))

        model_info = cls(
            alias=alias,
            name=name,
            assistant_role=assistant_role,
            integration=integration,
            system_supported=system_supported,
            user_role=user_role,
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
