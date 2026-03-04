from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_authentication_type import CustomAuthenticationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0
    from ..models.custom_llm_config import CustomLLMConfig
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig


T = TypeVar("T", bound="CustomIntegration")


@_attrs_define
class CustomIntegration:
    """Read model for custom integrations.

    api_key_value is not stored in extra (it's encrypted in the token column),
    so we override the parent validator to skip requiring it on read.

    Attributes
    ----------
            models (list[str]): List of model names for the custom integration
            endpoint (str): Endpoint URL for the custom integration.
            multi_modal_config (Union['MultiModalModelIntegrationConfig', None, Unset]): Configuration for multi-modal (file
                upload) capabilities.
            authentication_type (Union[Unset, CustomAuthenticationType]): Authentication types for custom integrations.

                Values:
                - none: No authentication required
                - oauth2: OAuth2 token-based authentication
                - api_key: API key header-based authentication
            default_model (Union[None, Unset, str]): Default model to use. If not provided, defaults to the first model in
                the models list.
            authentication_scope (Union[None, Unset, str]): Optional scope for OAuth2 authentication.
            oauth2_token_url (Union[None, Unset, str]): OAuth2 token URL for custom OAuth2 authentication. If not provided,
                defaults to the endpoint.
            api_key_header (Union[None, Unset, str]): HTTP header name to use for API key authentication (e.g., 'X-API-Key',
                'Authorization').
            api_key_value (Union[None, Unset, str]): API key value to send in the specified header for authentication.
            custom_llm_config (Union['CustomLLMConfig', None, Unset]): Optional configuration for a custom LiteLLM handler
                class. When specified, the handler's acompletion() method is used instead of the default litellm.acompletion().
            id (Union[None, Unset, str]):
            name (Union[Literal['custom'], Unset]):  Default: 'custom'.
            extra (Union['CustomIntegrationExtraType0', None, Unset]):
    """

    models: list[str]
    endpoint: str
    multi_modal_config: Union["MultiModalModelIntegrationConfig", None, Unset] = UNSET
    authentication_type: Union[Unset, CustomAuthenticationType] = UNSET
    default_model: Union[None, Unset, str] = UNSET
    authentication_scope: Union[None, Unset, str] = UNSET
    oauth2_token_url: Union[None, Unset, str] = UNSET
    api_key_header: Union[None, Unset, str] = UNSET
    api_key_value: Union[None, Unset, str] = UNSET
    custom_llm_config: Union["CustomLLMConfig", None, Unset] = UNSET
    id: Union[None, Unset, str] = UNSET
    name: Union[Literal["custom"], Unset] = "custom"
    extra: Union["CustomIntegrationExtraType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0
        from ..models.custom_llm_config import CustomLLMConfig
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        models = self.models

        endpoint = self.endpoint

        multi_modal_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.multi_modal_config, Unset):
            multi_modal_config = UNSET
        elif isinstance(self.multi_modal_config, MultiModalModelIntegrationConfig):
            multi_modal_config = self.multi_modal_config.to_dict()
        else:
            multi_modal_config = self.multi_modal_config

        authentication_type: Union[Unset, str] = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value

        default_model: Union[None, Unset, str]
        default_model = UNSET if isinstance(self.default_model, Unset) else self.default_model

        authentication_scope: Union[None, Unset, str]
        authentication_scope = UNSET if isinstance(self.authentication_scope, Unset) else self.authentication_scope

        oauth2_token_url: Union[None, Unset, str]
        oauth2_token_url = UNSET if isinstance(self.oauth2_token_url, Unset) else self.oauth2_token_url

        api_key_header: Union[None, Unset, str]
        api_key_header = UNSET if isinstance(self.api_key_header, Unset) else self.api_key_header

        api_key_value: Union[None, Unset, str]
        api_key_value = UNSET if isinstance(self.api_key_value, Unset) else self.api_key_value

        custom_llm_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.custom_llm_config, Unset):
            custom_llm_config = UNSET
        elif isinstance(self.custom_llm_config, CustomLLMConfig):
            custom_llm_config = self.custom_llm_config.to_dict()
        else:
            custom_llm_config = self.custom_llm_config

        id: Union[None, Unset, str]
        id = UNSET if isinstance(self.id, Unset) else self.id

        name = self.name

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, CustomIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"models": models, "endpoint": endpoint})
        if multi_modal_config is not UNSET:
            field_dict["multi_modal_config"] = multi_modal_config
        if authentication_type is not UNSET:
            field_dict["authentication_type"] = authentication_type
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if authentication_scope is not UNSET:
            field_dict["authentication_scope"] = authentication_scope
        if oauth2_token_url is not UNSET:
            field_dict["oauth2_token_url"] = oauth2_token_url
        if api_key_header is not UNSET:
            field_dict["api_key_header"] = api_key_header
        if api_key_value is not UNSET:
            field_dict["api_key_value"] = api_key_value
        if custom_llm_config is not UNSET:
            field_dict["custom_llm_config"] = custom_llm_config
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0
        from ..models.custom_llm_config import CustomLLMConfig
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        d = dict(src_dict)
        models = cast(list[str], d.pop("models"))

        endpoint = d.pop("endpoint")

        def _parse_multi_modal_config(data: object) -> Union["MultiModalModelIntegrationConfig", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MultiModalModelIntegrationConfig.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["MultiModalModelIntegrationConfig", None, Unset], data)

        multi_modal_config = _parse_multi_modal_config(d.pop("multi_modal_config", UNSET))

        _authentication_type = d.pop("authentication_type", UNSET)
        authentication_type: Union[Unset, CustomAuthenticationType]
        if isinstance(_authentication_type, Unset):
            authentication_type = UNSET
        else:
            authentication_type = CustomAuthenticationType(_authentication_type)

        def _parse_default_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_model = _parse_default_model(d.pop("default_model", UNSET))

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

        def _parse_api_key_header(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_key_header = _parse_api_key_header(d.pop("api_key_header", UNSET))

        def _parse_api_key_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_key_value = _parse_api_key_value(d.pop("api_key_value", UNSET))

        def _parse_custom_llm_config(data: object) -> Union["CustomLLMConfig", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomLLMConfig.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CustomLLMConfig", None, Unset], data)

        custom_llm_config = _parse_custom_llm_config(d.pop("custom_llm_config", UNSET))

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        name = cast(Union[Literal["custom"], Unset], d.pop("name", UNSET))
        if name != "custom" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'custom', got '{name}'")

        def _parse_extra(data: object) -> Union["CustomIntegrationExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomIntegrationExtraType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CustomIntegrationExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        custom_integration = cls(
            models=models,
            endpoint=endpoint,
            multi_modal_config=multi_modal_config,
            authentication_type=authentication_type,
            default_model=default_model,
            authentication_scope=authentication_scope,
            oauth2_token_url=oauth2_token_url,
            api_key_header=api_key_header,
            api_key_value=api_key_value,
            custom_llm_config=custom_llm_config,
            id=id,
            name=name,
            extra=extra,
        )

        custom_integration.additional_properties = d
        return custom_integration

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
