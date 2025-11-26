from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.anthropic_authentication_type import AnthropicAuthenticationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.anthropic_integration_create_custom_header_mapping_type_0 import (
        AnthropicIntegrationCreateCustomHeaderMappingType0,
    )


T = TypeVar("T", bound="AnthropicIntegrationCreate")


@_attrs_define
class AnthropicIntegrationCreate:
    """
    Attributes
    ----------
        token (str):
        authentication_type (Union[Unset, AnthropicAuthenticationType]):
        endpoint (Union[None, Unset, str]): Custom base URL for the Anthropic API. Required if `proxy` is True.
        authentication_scope (Union[None, Unset, str]):
        oauth2_token_url (Union[None, Unset, str]): OAuth2 token URL for custom OAuth2 authentication
        custom_header_mapping (Union['AnthropicIntegrationCreateCustomHeaderMappingType0', None, Unset]): Custom header
            mapping from internal fields to be included in the LLM request.
    """

    token: str
    authentication_type: Union[Unset, AnthropicAuthenticationType] = UNSET
    endpoint: Union[None, Unset, str] = UNSET
    authentication_scope: Union[None, Unset, str] = UNSET
    oauth2_token_url: Union[None, Unset, str] = UNSET
    custom_header_mapping: Union["AnthropicIntegrationCreateCustomHeaderMappingType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.anthropic_integration_create_custom_header_mapping_type_0 import (
            AnthropicIntegrationCreateCustomHeaderMappingType0,
        )

        token = self.token

        authentication_type: Union[Unset, str] = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value

        endpoint: Union[None, Unset, str]
        endpoint = UNSET if isinstance(self.endpoint, Unset) else self.endpoint

        authentication_scope: Union[None, Unset, str]
        authentication_scope = UNSET if isinstance(self.authentication_scope, Unset) else self.authentication_scope

        oauth2_token_url: Union[None, Unset, str]
        oauth2_token_url = UNSET if isinstance(self.oauth2_token_url, Unset) else self.oauth2_token_url

        custom_header_mapping: Union[None, Unset, dict[str, Any]]
        if isinstance(self.custom_header_mapping, Unset):
            custom_header_mapping = UNSET
        elif isinstance(self.custom_header_mapping, AnthropicIntegrationCreateCustomHeaderMappingType0):
            custom_header_mapping = self.custom_header_mapping.to_dict()
        else:
            custom_header_mapping = self.custom_header_mapping

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"token": token})
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.anthropic_integration_create_custom_header_mapping_type_0 import (
            AnthropicIntegrationCreateCustomHeaderMappingType0,
        )

        d = dict(src_dict)
        token = d.pop("token")

        _authentication_type = d.pop("authentication_type", UNSET)
        authentication_type: Union[Unset, AnthropicAuthenticationType]
        if isinstance(_authentication_type, Unset):
            authentication_type = UNSET
        else:
            authentication_type = AnthropicAuthenticationType(_authentication_type)

        def _parse_endpoint(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        endpoint = _parse_endpoint(d.pop("endpoint", UNSET))

        def _parse_authentication_scope(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        authentication_scope = _parse_authentication_scope(d.pop("authentication_scope", UNSET))

        def _parse_oauth2_token_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        oauth2_token_url = _parse_oauth2_token_url(d.pop("oauth2_token_url", UNSET))

        def _parse_custom_header_mapping(
            data: object,
        ) -> Union["AnthropicIntegrationCreateCustomHeaderMappingType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnthropicIntegrationCreateCustomHeaderMappingType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AnthropicIntegrationCreateCustomHeaderMappingType0", None, Unset], data)

        custom_header_mapping = _parse_custom_header_mapping(d.pop("custom_header_mapping", UNSET))

        anthropic_integration_create = cls(
            token=token,
            authentication_type=authentication_type,
            endpoint=endpoint,
            authentication_scope=authentication_scope,
            oauth2_token_url=oauth2_token_url,
            custom_header_mapping=custom_header_mapping,
        )

        anthropic_integration_create.additional_properties = d
        return anthropic_integration_create

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
