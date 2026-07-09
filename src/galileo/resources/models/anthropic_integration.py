from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.anthropic_authentication_type import AnthropicAuthenticationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.anthropic_integration_custom_header_mapping_type_0 import AnthropicIntegrationCustomHeaderMappingType0
    from ..models.anthropic_integration_extra_type_0 import AnthropicIntegrationExtraType0
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig


T = TypeVar("T", bound="AnthropicIntegration")


@_attrs_define
class AnthropicIntegration:
    """
    Attributes:
        multi_modal_config (MultiModalModelIntegrationConfig | None | Unset): Configuration for multi-modal (file
            upload) capabilities.
        authentication_type (AnthropicAuthenticationType | Unset):
        endpoint (None | str | Unset): Custom base URL for the Anthropic API. Required if `proxy` is True.
        authentication_scope (None | str | Unset):
        oauth2_token_url (None | str | Unset): OAuth2 token URL for custom OAuth2 authentication
        custom_header_mapping (AnthropicIntegrationCustomHeaderMappingType0 | None | Unset): Custom header mapping from
            internal fields to be included in the LLM request.
        id (None | str | Unset):
        name (Literal['anthropic'] | Unset):  Default: 'anthropic'.
        extra (AnthropicIntegrationExtraType0 | None | Unset):
    """

    multi_modal_config: MultiModalModelIntegrationConfig | None | Unset = UNSET
    authentication_type: AnthropicAuthenticationType | Unset = UNSET
    endpoint: None | str | Unset = UNSET
    authentication_scope: None | str | Unset = UNSET
    oauth2_token_url: None | str | Unset = UNSET
    custom_header_mapping: AnthropicIntegrationCustomHeaderMappingType0 | None | Unset = UNSET
    id: None | str | Unset = UNSET
    name: Literal["anthropic"] | Unset = "anthropic"
    extra: AnthropicIntegrationExtraType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.anthropic_integration_custom_header_mapping_type_0 import (
            AnthropicIntegrationCustomHeaderMappingType0,
        )
        from ..models.anthropic_integration_extra_type_0 import AnthropicIntegrationExtraType0
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        multi_modal_config: dict[str, Any] | None | Unset
        if isinstance(self.multi_modal_config, Unset):
            multi_modal_config = UNSET
        elif isinstance(self.multi_modal_config, MultiModalModelIntegrationConfig):
            multi_modal_config = self.multi_modal_config.to_dict()
        else:
            multi_modal_config = self.multi_modal_config

        authentication_type: str | Unset = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value

        endpoint: None | str | Unset
        if isinstance(self.endpoint, Unset):
            endpoint = UNSET
        else:
            endpoint = self.endpoint

        authentication_scope: None | str | Unset
        if isinstance(self.authentication_scope, Unset):
            authentication_scope = UNSET
        else:
            authentication_scope = self.authentication_scope

        oauth2_token_url: None | str | Unset
        if isinstance(self.oauth2_token_url, Unset):
            oauth2_token_url = UNSET
        else:
            oauth2_token_url = self.oauth2_token_url

        custom_header_mapping: dict[str, Any] | None | Unset
        if isinstance(self.custom_header_mapping, Unset):
            custom_header_mapping = UNSET
        elif isinstance(self.custom_header_mapping, AnthropicIntegrationCustomHeaderMappingType0):
            custom_header_mapping = self.custom_header_mapping.to_dict()
        else:
            custom_header_mapping = self.custom_header_mapping

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name = self.name

        extra: dict[str, Any] | None | Unset
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, AnthropicIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if multi_modal_config is not UNSET:
            field_dict["multi_modal_config"] = multi_modal_config
        if authentication_type is not UNSET:
            field_dict["authentication_type"] = authentication_type
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if authentication_scope is not UNSET:
            field_dict["authentication_scope"] = authentication_scope
        if oauth2_token_url is not UNSET:
            field_dict["oauth2_token_url"] = oauth2_token_url
        if custom_header_mapping is not UNSET:
            field_dict["custom_header_mapping"] = custom_header_mapping
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.anthropic_integration_custom_header_mapping_type_0 import (
            AnthropicIntegrationCustomHeaderMappingType0,
        )
        from ..models.anthropic_integration_extra_type_0 import AnthropicIntegrationExtraType0
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        d = dict(src_dict)

        def _parse_multi_modal_config(data: object) -> MultiModalModelIntegrationConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                multi_modal_config_type_0 = MultiModalModelIntegrationConfig.from_dict(data)

                return multi_modal_config_type_0
            except:  # noqa: E722
                pass
            return cast(MultiModalModelIntegrationConfig | None | Unset, data)

        multi_modal_config = _parse_multi_modal_config(d.pop("multi_modal_config", UNSET))

        _authentication_type = d.pop("authentication_type", UNSET)
        authentication_type: AnthropicAuthenticationType | Unset
        if isinstance(_authentication_type, Unset):
            authentication_type = UNSET
        else:
            authentication_type = AnthropicAuthenticationType(_authentication_type)

        def _parse_endpoint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        endpoint = _parse_endpoint(d.pop("endpoint", UNSET))

        def _parse_authentication_scope(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        authentication_scope = _parse_authentication_scope(d.pop("authentication_scope", UNSET))

        def _parse_oauth2_token_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        oauth2_token_url = _parse_oauth2_token_url(d.pop("oauth2_token_url", UNSET))

        def _parse_custom_header_mapping(data: object) -> AnthropicIntegrationCustomHeaderMappingType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                custom_header_mapping_type_0 = AnthropicIntegrationCustomHeaderMappingType0.from_dict(data)

                return custom_header_mapping_type_0
            except:  # noqa: E722
                pass
            return cast(AnthropicIntegrationCustomHeaderMappingType0 | None | Unset, data)

        custom_header_mapping = _parse_custom_header_mapping(d.pop("custom_header_mapping", UNSET))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        name = cast(Literal["anthropic"] | Unset, d.pop("name", UNSET))
        if name != "anthropic" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'anthropic', got '{name}'")

        def _parse_extra(data: object) -> AnthropicIntegrationExtraType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = AnthropicIntegrationExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(AnthropicIntegrationExtraType0 | None | Unset, data)

        extra = _parse_extra(d.pop("extra", UNSET))

        anthropic_integration = cls(
            multi_modal_config=multi_modal_config,
            authentication_type=authentication_type,
            endpoint=endpoint,
            authentication_scope=authentication_scope,
            oauth2_token_url=oauth2_token_url,
            custom_header_mapping=custom_header_mapping,
            id=id,
            name=name,
            extra=extra,
        )

        anthropic_integration.additional_properties = d
        return anthropic_integration

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
