from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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


T = TypeVar("T", bound="AzureIntegrationCreate")


@_attrs_define
class AzureIntegrationCreate:
    """
    Attributes
    ----------
        endpoint (str):
        token (str):
        api_version (Union[Unset, str]):  Default: '2025-03-01-preview'.
        authentication_scope (Union[None, Unset, str]):
        authentication_type (Union[Unset, AzureAuthenticationType]):
        available_deployments (Union[None, Unset, list['AzureModelDeployment']]): The available deployments for this
            integration. If provided, we will not try to get this list from Azure.
        azure_deployment (Union[None, Unset, str]):
        custom_header_mapping (Union['AzureIntegrationCreateCustomHeaderMappingType0', None, Unset]): Custom header
            mapping from internal fields to be included in the LLM request.
        default_headers (Union['AzureIntegrationCreateDefaultHeadersType0', None, Unset]):
        deployments (Union[Unset, AzureIntegrationCreateDeployments]):
        oauth2_token_url (Union[None, Unset, str]): OAuth2 token URL for custom OAuth2 authentication
        proxy (Union[Unset, bool]):  Default: False.
    """

    endpoint: str
    token: str
    api_version: Union[Unset, str] = "2025-03-01-preview"
    authentication_scope: Union[None, Unset, str] = UNSET
    authentication_type: Union[Unset, AzureAuthenticationType] = UNSET
    available_deployments: Union[None, Unset, list["AzureModelDeployment"]] = UNSET
    azure_deployment: Union[None, Unset, str] = UNSET
    custom_header_mapping: Union["AzureIntegrationCreateCustomHeaderMappingType0", None, Unset] = UNSET
    default_headers: Union["AzureIntegrationCreateDefaultHeadersType0", None, Unset] = UNSET
    deployments: Union[Unset, "AzureIntegrationCreateDeployments"] = UNSET
    oauth2_token_url: Union[None, Unset, str] = UNSET
    proxy: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.azure_integration_create_custom_header_mapping_type_0 import (
            AzureIntegrationCreateCustomHeaderMappingType0,
        )
        from ..models.azure_integration_create_default_headers_type_0 import AzureIntegrationCreateDefaultHeadersType0

        endpoint = self.endpoint

        token = self.token

        api_version = self.api_version

        authentication_scope: Union[None, Unset, str]
        authentication_scope = UNSET if isinstance(self.authentication_scope, Unset) else self.authentication_scope

        authentication_type: Union[Unset, str] = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value

        available_deployments: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.available_deployments, Unset):
            available_deployments = UNSET
        elif isinstance(self.available_deployments, list):
            available_deployments = []
            for available_deployments_type_0_item_data in self.available_deployments:
                available_deployments_type_0_item = available_deployments_type_0_item_data.to_dict()
                available_deployments.append(available_deployments_type_0_item)

        else:
            available_deployments = self.available_deployments

        azure_deployment: Union[None, Unset, str]
        azure_deployment = UNSET if isinstance(self.azure_deployment, Unset) else self.azure_deployment

        custom_header_mapping: Union[None, Unset, dict[str, Any]]
        if isinstance(self.custom_header_mapping, Unset):
            custom_header_mapping = UNSET
        elif isinstance(self.custom_header_mapping, AzureIntegrationCreateCustomHeaderMappingType0):
            custom_header_mapping = self.custom_header_mapping.to_dict()
        else:
            custom_header_mapping = self.custom_header_mapping

        default_headers: Union[None, Unset, dict[str, Any]]
        if isinstance(self.default_headers, Unset):
            default_headers = UNSET
        elif isinstance(self.default_headers, AzureIntegrationCreateDefaultHeadersType0):
            default_headers = self.default_headers.to_dict()
        else:
            default_headers = self.default_headers

        deployments: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.deployments, Unset):
            deployments = self.deployments.to_dict()

        oauth2_token_url: Union[None, Unset, str]
        oauth2_token_url = UNSET if isinstance(self.oauth2_token_url, Unset) else self.oauth2_token_url

        proxy = self.proxy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"endpoint": endpoint, "token": token})
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if authentication_scope is not UNSET:
            field_dict["authentication_scope"] = authentication_scope
        if authentication_type is not UNSET:
            field_dict["authentication_type"] = authentication_type
        if available_deployments is not UNSET:
            field_dict["available_deployments"] = available_deployments
        if azure_deployment is not UNSET:
            field_dict["azure_deployment"] = azure_deployment
        if custom_header_mapping is not UNSET:
            field_dict["custom_header_mapping"] = custom_header_mapping
        if default_headers is not UNSET:
            field_dict["default_headers"] = default_headers
        if deployments is not UNSET:
            field_dict["deployments"] = deployments
        if oauth2_token_url is not UNSET:
            field_dict["oauth2_token_url"] = oauth2_token_url
        if proxy is not UNSET:
            field_dict["proxy"] = proxy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.azure_integration_create_custom_header_mapping_type_0 import (
            AzureIntegrationCreateCustomHeaderMappingType0,
        )
        from ..models.azure_integration_create_default_headers_type_0 import AzureIntegrationCreateDefaultHeadersType0
        from ..models.azure_integration_create_deployments import AzureIntegrationCreateDeployments
        from ..models.azure_model_deployment import AzureModelDeployment

        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        token = d.pop("token")

        api_version = d.pop("api_version", UNSET)

        def _parse_authentication_scope(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        authentication_scope = _parse_authentication_scope(d.pop("authentication_scope", UNSET))

        _authentication_type = d.pop("authentication_type", UNSET)
        authentication_type: Union[Unset, AzureAuthenticationType]
        if isinstance(_authentication_type, Unset):
            authentication_type = UNSET
        else:
            authentication_type = AzureAuthenticationType(_authentication_type)

        def _parse_available_deployments(data: object) -> Union[None, Unset, list["AzureModelDeployment"]]:
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
            return cast(Union[None, Unset, list["AzureModelDeployment"]], data)

        available_deployments = _parse_available_deployments(d.pop("available_deployments", UNSET))

        def _parse_azure_deployment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        azure_deployment = _parse_azure_deployment(d.pop("azure_deployment", UNSET))

        def _parse_custom_header_mapping(
            data: object,
        ) -> Union["AzureIntegrationCreateCustomHeaderMappingType0", None, Unset]:
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
            return cast(Union["AzureIntegrationCreateCustomHeaderMappingType0", None, Unset], data)

        custom_header_mapping = _parse_custom_header_mapping(d.pop("custom_header_mapping", UNSET))

        def _parse_default_headers(data: object) -> Union["AzureIntegrationCreateDefaultHeadersType0", None, Unset]:
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
            return cast(Union["AzureIntegrationCreateDefaultHeadersType0", None, Unset], data)

        default_headers = _parse_default_headers(d.pop("default_headers", UNSET))

        _deployments = d.pop("deployments", UNSET)
        deployments: Union[Unset, AzureIntegrationCreateDeployments]
        if isinstance(_deployments, Unset):
            deployments = UNSET
        else:
            deployments = AzureIntegrationCreateDeployments.from_dict(_deployments)

        def _parse_oauth2_token_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        oauth2_token_url = _parse_oauth2_token_url(d.pop("oauth2_token_url", UNSET))

        proxy = d.pop("proxy", UNSET)

        azure_integration_create = cls(
            endpoint=endpoint,
            token=token,
            api_version=api_version,
            authentication_scope=authentication_scope,
            authentication_type=authentication_type,
            available_deployments=available_deployments,
            azure_deployment=azure_deployment,
            custom_header_mapping=custom_header_mapping,
            default_headers=default_headers,
            deployments=deployments,
            oauth2_token_url=oauth2_token_url,
            proxy=proxy,
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
