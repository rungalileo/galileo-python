from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.azure_authentication_type import AzureAuthenticationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.azure_integration_create_custom_header_mapping_type_0 import (
        AzureIntegrationCreateCustomHeaderMappingType0,
    )
    from ..models.azure_integration_create_default_headers_type_0 import AzureIntegrationCreateDefaultHeadersType0
    from ..models.azure_integration_create_deployments import AzureIntegrationCreateDeployments
    from ..models.azure_model_deployment import AzureModelDeployment
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig


T = TypeVar("T", bound="AzureIntegrationCreate")


@_attrs_define
class AzureIntegrationCreate:
    """
    Attributes
    ----------
        endpoint (str):
        token (str):
        multi_modal_config (MultiModalModelIntegrationConfig | None | Unset): Configuration for multi-modal (file
            upload) capabilities.
        proxy (bool | Unset):  Default: False.
        api_version (str | Unset):  Default: '2025-03-01-preview'.
        azure_deployment (None | str | Unset):
        authentication_type (AzureAuthenticationType | Unset):
        authentication_scope (None | str | Unset):
        default_headers (AzureIntegrationCreateDefaultHeadersType0 | None | Unset):
        deployments (AzureIntegrationCreateDeployments | Unset):
        oauth2_token_url (None | str | Unset): OAuth2 token URL for custom OAuth2 authentication
        custom_header_mapping (AzureIntegrationCreateCustomHeaderMappingType0 | None | Unset): Custom header mapping
            from internal fields to be included in the LLM request.
        available_deployments (list[AzureModelDeployment] | None | Unset): The available deployments for this
            integration. If provided, we will not try to get this list from Azure.
    """

    endpoint: str
    token: str
    multi_modal_config: MultiModalModelIntegrationConfig | None | Unset = UNSET
    proxy: bool | Unset = False
    api_version: str | Unset = "2025-03-01-preview"
    azure_deployment: None | str | Unset = UNSET
    authentication_type: AzureAuthenticationType | Unset = UNSET
    authentication_scope: None | str | Unset = UNSET
    default_headers: AzureIntegrationCreateDefaultHeadersType0 | None | Unset = UNSET
    deployments: AzureIntegrationCreateDeployments | Unset = UNSET
    oauth2_token_url: None | str | Unset = UNSET
    custom_header_mapping: AzureIntegrationCreateCustomHeaderMappingType0 | None | Unset = UNSET
    available_deployments: list[AzureModelDeployment] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.azure_integration_create_custom_header_mapping_type_0 import (
            AzureIntegrationCreateCustomHeaderMappingType0,
        )
        from ..models.azure_integration_create_default_headers_type_0 import AzureIntegrationCreateDefaultHeadersType0
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        endpoint = self.endpoint

        token = self.token

        multi_modal_config: dict[str, Any] | None | Unset
        if isinstance(self.multi_modal_config, Unset):
            multi_modal_config = UNSET
        elif isinstance(self.multi_modal_config, MultiModalModelIntegrationConfig):
            multi_modal_config = self.multi_modal_config.to_dict()
        else:
            multi_modal_config = self.multi_modal_config

        proxy = self.proxy

        api_version = self.api_version

        azure_deployment: None | str | Unset
        azure_deployment = UNSET if isinstance(self.azure_deployment, Unset) else self.azure_deployment

        authentication_type: str | Unset = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value

        authentication_scope: None | str | Unset
        authentication_scope = UNSET if isinstance(self.authentication_scope, Unset) else self.authentication_scope

        default_headers: dict[str, Any] | None | Unset
        if isinstance(self.default_headers, Unset):
            default_headers = UNSET
        elif isinstance(self.default_headers, AzureIntegrationCreateDefaultHeadersType0):
            default_headers = self.default_headers.to_dict()
        else:
            default_headers = self.default_headers

        deployments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deployments, Unset):
            deployments = self.deployments.to_dict()

        oauth2_token_url: None | str | Unset
        oauth2_token_url = UNSET if isinstance(self.oauth2_token_url, Unset) else self.oauth2_token_url

        custom_header_mapping: dict[str, Any] | None | Unset
        if isinstance(self.custom_header_mapping, Unset):
            custom_header_mapping = UNSET
        elif isinstance(self.custom_header_mapping, AzureIntegrationCreateCustomHeaderMappingType0):
            custom_header_mapping = self.custom_header_mapping.to_dict()
        else:
            custom_header_mapping = self.custom_header_mapping

        available_deployments: list[dict[str, Any]] | None | Unset
        if isinstance(self.available_deployments, Unset):
            available_deployments = UNSET
        elif isinstance(self.available_deployments, list):
            available_deployments = []
            for available_deployments_type_0_item_data in self.available_deployments:
                available_deployments_type_0_item = available_deployments_type_0_item_data.to_dict()
                available_deployments.append(available_deployments_type_0_item)

        else:
            available_deployments = self.available_deployments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"endpoint": endpoint, "token": token})
        if multi_modal_config is not UNSET:
            field_dict["multi_modal_config"] = multi_modal_config
        if proxy is not UNSET:
            field_dict["proxy"] = proxy
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if azure_deployment is not UNSET:
            field_dict["azure_deployment"] = azure_deployment
        if authentication_type is not UNSET:
            field_dict["authentication_type"] = authentication_type
        if authentication_scope is not UNSET:
            field_dict["authentication_scope"] = authentication_scope
        if default_headers is not UNSET:
            field_dict["default_headers"] = default_headers
        if deployments is not UNSET:
            field_dict["deployments"] = deployments
        if oauth2_token_url is not UNSET:
            field_dict["oauth2_token_url"] = oauth2_token_url
        if custom_header_mapping is not UNSET:
            field_dict["custom_header_mapping"] = custom_header_mapping
        if available_deployments is not UNSET:
            field_dict["available_deployments"] = available_deployments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.azure_integration_create_custom_header_mapping_type_0 import (
            AzureIntegrationCreateCustomHeaderMappingType0,
        )
        from ..models.azure_integration_create_default_headers_type_0 import AzureIntegrationCreateDefaultHeadersType0
        from ..models.azure_integration_create_deployments import AzureIntegrationCreateDeployments
        from ..models.azure_model_deployment import AzureModelDeployment
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        token = d.pop("token")

        def _parse_multi_modal_config(data: object) -> MultiModalModelIntegrationConfig | None | Unset:
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
            return cast(MultiModalModelIntegrationConfig | None | Unset, data)

        multi_modal_config = _parse_multi_modal_config(d.pop("multi_modal_config", UNSET))

        proxy = d.pop("proxy", UNSET)

        api_version = d.pop("api_version", UNSET)

        def _parse_azure_deployment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        azure_deployment = _parse_azure_deployment(d.pop("azure_deployment", UNSET))

        _authentication_type = d.pop("authentication_type", UNSET)
        authentication_type: AzureAuthenticationType | Unset
        if isinstance(_authentication_type, Unset):
            authentication_type = UNSET
        else:
            authentication_type = AzureAuthenticationType(_authentication_type)

        def _parse_authentication_scope(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        authentication_scope = _parse_authentication_scope(d.pop("authentication_scope", UNSET))

        def _parse_default_headers(data: object) -> AzureIntegrationCreateDefaultHeadersType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AzureIntegrationCreateDefaultHeadersType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(AzureIntegrationCreateDefaultHeadersType0 | None | Unset, data)

        default_headers = _parse_default_headers(d.pop("default_headers", UNSET))

        _deployments = d.pop("deployments", UNSET)
        deployments: AzureIntegrationCreateDeployments | Unset
        if isinstance(_deployments, Unset):
            deployments = UNSET
        else:
            deployments = AzureIntegrationCreateDeployments.from_dict(_deployments)

        def _parse_oauth2_token_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        oauth2_token_url = _parse_oauth2_token_url(d.pop("oauth2_token_url", UNSET))

        def _parse_custom_header_mapping(data: object) -> AzureIntegrationCreateCustomHeaderMappingType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AzureIntegrationCreateCustomHeaderMappingType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(AzureIntegrationCreateCustomHeaderMappingType0 | None | Unset, data)

        custom_header_mapping = _parse_custom_header_mapping(d.pop("custom_header_mapping", UNSET))

        def _parse_available_deployments(data: object) -> list[AzureModelDeployment] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                available_deployments_type_0 = []
                _available_deployments_type_0 = data
                for available_deployments_type_0_item_data in _available_deployments_type_0:
                    available_deployments_type_0_item = AzureModelDeployment.from_dict(
                        available_deployments_type_0_item_data
                    )

                    available_deployments_type_0.append(available_deployments_type_0_item)

                return available_deployments_type_0
            except:  # noqa: E722
                pass
            return cast(list[AzureModelDeployment] | None | Unset, data)

        available_deployments = _parse_available_deployments(d.pop("available_deployments", UNSET))

        azure_integration_create = cls(
            endpoint=endpoint,
            token=token,
            multi_modal_config=multi_modal_config,
            proxy=proxy,
            api_version=api_version,
            azure_deployment=azure_deployment,
            authentication_type=authentication_type,
            authentication_scope=authentication_scope,
            default_headers=default_headers,
            deployments=deployments,
            oauth2_token_url=oauth2_token_url,
            custom_header_mapping=custom_header_mapping,
            available_deployments=available_deployments,
        )

        azure_integration_create.additional_properties = d
        return azure_integration_create

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
