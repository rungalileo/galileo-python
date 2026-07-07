from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_authentication_type import CustomAuthenticationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_integration_custom_header_mapping_type_0 import CustomIntegrationCustomHeaderMappingType0
    from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0
    from ..models.custom_integration_headers_type_0 import CustomIntegrationHeadersType0
    from ..models.custom_integration_model_properties import CustomIntegrationModelProperties
    from ..models.custom_llm_config import CustomLLMConfig
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig


T = TypeVar("T", bound="CustomIntegration")


@_attrs_define
class CustomIntegration:
    """Read model for custom integrations.

    api_key_value is not stored in extra (it's encrypted in the token column),
    so we override the parent validator to skip requiring it on read.
    Headers are not returned on read (they're encrypted and sensitive).

        Attributes:
            endpoint (str): Endpoint URL for the custom integration.
            multi_modal_config (Union['MultiModalModelIntegrationConfig', None, Unset]): Configuration for multi-modal (file
                upload) capabilities.
            authentication_type (Union[Unset, CustomAuthenticationType]): Authentication types for custom integrations.

                Values:
                - none: No authentication required
                - oauth2: OAuth2 token-based authentication
                - api_key: API key header-based authentication
            models (Union[None, Unset, list[str]]): List of model names for the custom integration. Deprecated: use
                model_properties instead.
            model_properties (Union[None, Unset, list['CustomIntegrationModelProperties']]): List of model properties with
                name and alias for the custom integration.
            is_legacy_format (Union[Unset, bool]): Internal: whether this config was created from the legacy 'models' field.
                Default: False.
            default_model (Union[None, Unset, str]): Default model to use. If not provided, defaults to the first model.
            authentication_scope (Union[None, Unset, str]): Optional scope for OAuth2 authentication.
            oauth2_token_url (Union[None, Unset, str]): OAuth2 token URL for custom OAuth2 authentication. If not provided,
                defaults to the endpoint.
            api_key_header (Union[None, Unset, str]): HTTP header name to use for API key authentication (e.g., 'X-API-Key',
                'Authorization').
            api_key_value (Union[None, Unset, str]): API key value to send in the specified header for authentication.
            custom_llm_config (Union['CustomLLMConfig', None, Unset]): Optional configuration for a custom LiteLLM handler
                class. When specified, the handler's acompletion() method is used instead of the default litellm.acompletion().
            custom_header_mapping (Union['CustomIntegrationCustomHeaderMappingType0', None, Unset]): Custom header mapping
                from internal fields (job_id, user_id, project_id, run_id) to custom header names to be included in LLM
                requests.
            headers (Union['CustomIntegrationHeadersType0', None, Unset]):
            id (Union[None, Unset, str]):
            name (Union[Unset, str]):  Default: 'custom'.
            provider (Union[Literal['custom'], Unset]):  Default: 'custom'.
            extra (Union['CustomIntegrationExtraType0', None, Unset]):
    """

    endpoint: str
    multi_modal_config: Union["MultiModalModelIntegrationConfig", None, Unset] = UNSET
    authentication_type: Union[Unset, CustomAuthenticationType] = UNSET
    models: Union[None, Unset, list[str]] = UNSET
    model_properties: Union[None, Unset, list["CustomIntegrationModelProperties"]] = UNSET
    is_legacy_format: Union[Unset, bool] = False
    default_model: Union[None, Unset, str] = UNSET
    authentication_scope: Union[None, Unset, str] = UNSET
    oauth2_token_url: Union[None, Unset, str] = UNSET
    api_key_header: Union[None, Unset, str] = UNSET
    api_key_value: Union[None, Unset, str] = UNSET
    custom_llm_config: Union["CustomLLMConfig", None, Unset] = UNSET
    custom_header_mapping: Union["CustomIntegrationCustomHeaderMappingType0", None, Unset] = UNSET
    headers: Union["CustomIntegrationHeadersType0", None, Unset] = UNSET
    id: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = "custom"
    provider: Union[Literal["custom"], Unset] = "custom"
    extra: Union["CustomIntegrationExtraType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.custom_integration_custom_header_mapping_type_0 import CustomIntegrationCustomHeaderMappingType0
        from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0
        from ..models.custom_integration_headers_type_0 import CustomIntegrationHeadersType0
        from ..models.custom_llm_config import CustomLLMConfig
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

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

        models: Union[None, Unset, list[str]]
        if isinstance(self.models, Unset):
            models = UNSET
        elif isinstance(self.models, list):
            models = self.models

        else:
            models = self.models

        model_properties: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.model_properties, Unset):
            model_properties = UNSET
        elif isinstance(self.model_properties, list):
            model_properties = []
            for model_properties_type_0_item_data in self.model_properties:
                model_properties_type_0_item = model_properties_type_0_item_data.to_dict()
                model_properties.append(model_properties_type_0_item)

        else:
            model_properties = self.model_properties

        is_legacy_format = self.is_legacy_format

        default_model: Union[None, Unset, str]
        if isinstance(self.default_model, Unset):
            default_model = UNSET
        else:
            default_model = self.default_model

        authentication_scope: Union[None, Unset, str]
        if isinstance(self.authentication_scope, Unset):
            authentication_scope = UNSET
        else:
            authentication_scope = self.authentication_scope

        oauth2_token_url: Union[None, Unset, str]
        if isinstance(self.oauth2_token_url, Unset):
            oauth2_token_url = UNSET
        else:
            oauth2_token_url = self.oauth2_token_url

        api_key_header: Union[None, Unset, str]
        if isinstance(self.api_key_header, Unset):
            api_key_header = UNSET
        else:
            api_key_header = self.api_key_header

        api_key_value: Union[None, Unset, str]
        if isinstance(self.api_key_value, Unset):
            api_key_value = UNSET
        else:
            api_key_value = self.api_key_value

        custom_llm_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.custom_llm_config, Unset):
            custom_llm_config = UNSET
        elif isinstance(self.custom_llm_config, CustomLLMConfig):
            custom_llm_config = self.custom_llm_config.to_dict()
        else:
            custom_llm_config = self.custom_llm_config

        custom_header_mapping: Union[None, Unset, dict[str, Any]]
        if isinstance(self.custom_header_mapping, Unset):
            custom_header_mapping = UNSET
        elif isinstance(self.custom_header_mapping, CustomIntegrationCustomHeaderMappingType0):
            custom_header_mapping = self.custom_header_mapping.to_dict()
        else:
            custom_header_mapping = self.custom_header_mapping

        headers: Union[None, Unset, dict[str, Any]]
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, CustomIntegrationHeadersType0):
            headers = self.headers.to_dict()
        else:
            headers = self.headers

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name = self.name

        provider = self.provider

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, CustomIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"endpoint": endpoint})
        if multi_modal_config is not UNSET:
            field_dict["multi_modal_config"] = multi_modal_config
        if authentication_type is not UNSET:
            field_dict["authentication_type"] = authentication_type
        if models is not UNSET:
            field_dict["models"] = models
        if model_properties is not UNSET:
            field_dict["model_properties"] = model_properties
        if is_legacy_format is not UNSET:
            field_dict["is_legacy_format"] = is_legacy_format
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
        if custom_header_mapping is not UNSET:
            field_dict["custom_header_mapping"] = custom_header_mapping
        if headers is not UNSET:
            field_dict["headers"] = headers
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if provider is not UNSET:
            field_dict["provider"] = provider
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_integration_custom_header_mapping_type_0 import CustomIntegrationCustomHeaderMappingType0
        from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0
        from ..models.custom_integration_headers_type_0 import CustomIntegrationHeadersType0
        from ..models.custom_integration_model_properties import CustomIntegrationModelProperties
        from ..models.custom_llm_config import CustomLLMConfig
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        def _parse_multi_modal_config(data: object) -> Union["MultiModalModelIntegrationConfig", None, Unset]:
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
            return cast(Union["MultiModalModelIntegrationConfig", None, Unset], data)

        multi_modal_config = _parse_multi_modal_config(d.pop("multi_modal_config", UNSET))

        _authentication_type = d.pop("authentication_type", UNSET)
        authentication_type: Union[Unset, CustomAuthenticationType]
        if isinstance(_authentication_type, Unset):
            authentication_type = UNSET
        else:
            authentication_type = CustomAuthenticationType(_authentication_type)

        def _parse_models(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                models_type_0 = cast(list[str], data)

                return models_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        models = _parse_models(d.pop("models", UNSET))

        def _parse_model_properties(data: object) -> Union[None, Unset, list["CustomIntegrationModelProperties"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                model_properties_type_0 = []
                _model_properties_type_0 = data
                for model_properties_type_0_item_data in _model_properties_type_0:
                    model_properties_type_0_item = CustomIntegrationModelProperties.from_dict(
                        model_properties_type_0_item_data
                    )

                    model_properties_type_0.append(model_properties_type_0_item)

                return model_properties_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CustomIntegrationModelProperties"]], data)

        model_properties = _parse_model_properties(d.pop("model_properties", UNSET))

        is_legacy_format = d.pop("is_legacy_format", UNSET)

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
                custom_llm_config_type_0 = CustomLLMConfig.from_dict(data)

                return custom_llm_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CustomLLMConfig", None, Unset], data)

        custom_llm_config = _parse_custom_llm_config(d.pop("custom_llm_config", UNSET))

        def _parse_custom_header_mapping(
            data: object,
        ) -> Union["CustomIntegrationCustomHeaderMappingType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                custom_header_mapping_type_0 = CustomIntegrationCustomHeaderMappingType0.from_dict(data)

                return custom_header_mapping_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CustomIntegrationCustomHeaderMappingType0", None, Unset], data)

        custom_header_mapping = _parse_custom_header_mapping(d.pop("custom_header_mapping", UNSET))

        def _parse_headers(data: object) -> Union["CustomIntegrationHeadersType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                headers_type_0 = CustomIntegrationHeadersType0.from_dict(data)

                return headers_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CustomIntegrationHeadersType0", None, Unset], data)

        headers = _parse_headers(d.pop("headers", UNSET))

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        name = d.pop("name", UNSET)

        provider = cast(Union[Literal["custom"], Unset], d.pop("provider", UNSET))
        if provider != "custom" and not isinstance(provider, Unset):
            raise ValueError(f"provider must match const 'custom', got '{provider}'")

        def _parse_extra(data: object) -> Union["CustomIntegrationExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = CustomIntegrationExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CustomIntegrationExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        custom_integration = cls(
            endpoint=endpoint,
            multi_modal_config=multi_modal_config,
            authentication_type=authentication_type,
            models=models,
            model_properties=model_properties,
            is_legacy_format=is_legacy_format,
            default_model=default_model,
            authentication_scope=authentication_scope,
            oauth2_token_url=oauth2_token_url,
            api_key_header=api_key_header,
            api_key_value=api_key_value,
            custom_llm_config=custom_llm_config,
            custom_header_mapping=custom_header_mapping,
            headers=headers,
            id=id,
            name=name,
            provider=provider,
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
