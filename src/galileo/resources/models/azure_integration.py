from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.azure_authentication_type import AzureAuthenticationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.azure_integration_custom_header_mapping_type_0 import AzureIntegrationCustomHeaderMappingType0
    from ..models.azure_integration_default_headers_type_0 import AzureIntegrationDefaultHeadersType0
    from ..models.azure_integration_deployments import AzureIntegrationDeployments
    from ..models.azure_integration_extra_type_0 import AzureIntegrationExtraType0
    from ..models.azure_model_deployment import AzureModelDeployment
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig


T = TypeVar("T", bound="AzureIntegration")


@_attrs_define
class AzureIntegration:
    """
    Attributes
    ----------
        endpoint (str):
        multi_modal_config (Union['MultiModalModelIntegrationConfig', None, Unset]): Configuration for multi-modal (file
            upload) capabilities.
        proxy (Union[Unset, bool]):  Default: False.
        api_version (Union[Unset, str]):  Default: '2025-03-01-preview'.
        azure_deployment (Union[None, Unset, str]):
        authentication_type (Union[Unset, AzureAuthenticationType]):
        authentication_scope (Union[None, Unset, str]):
        default_headers (Union['AzureIntegrationDefaultHeadersType0', None, Unset]):
        deployments (Union[Unset, AzureIntegrationDeployments]):
        oauth2_token_url (Union[None, Unset, str]): OAuth2 token URL for custom OAuth2 authentication
        custom_header_mapping (Union['AzureIntegrationCustomHeaderMappingType0', None, Unset]): Custom header mapping
            from internal fields to be included in the LLM request.
        available_deployments (Union[None, Unset, list['AzureModelDeployment']]): The available deployments for this
            integration. If provided, we will not try to get this list from Azure.
        id (Union[None, Unset, str]):
        name (Union[Literal['azure'], Unset]):  Default: 'azure'.
        extra (Union['AzureIntegrationExtraType0', None, Unset]):
    """

    endpoint: str
    multi_modal_config: Union["MultiModalModelIntegrationConfig", None, Unset] = UNSET
    proxy: Union[Unset, bool] = False
    api_version: Union[Unset, str] = "2025-03-01-preview"
    azure_deployment: Union[None, Unset, str] = UNSET
    authentication_type: Union[Unset, AzureAuthenticationType] = UNSET
    authentication_scope: Union[None, Unset, str] = UNSET
    default_headers: Union["AzureIntegrationDefaultHeadersType0", None, Unset] = UNSET
    deployments: Union[Unset, "AzureIntegrationDeployments"] = UNSET
    oauth2_token_url: Union[None, Unset, str] = UNSET
    custom_header_mapping: Union["AzureIntegrationCustomHeaderMappingType0", None, Unset] = UNSET
    available_deployments: Union[None, Unset, list["AzureModelDeployment"]] = UNSET
    id: Union[None, Unset, str] = UNSET
    name: Union[Literal["azure"], Unset] = "azure"
    extra: Union["AzureIntegrationExtraType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.azure_integration_custom_header_mapping_type_0 import AzureIntegrationCustomHeaderMappingType0
        from ..models.azure_integration_default_headers_type_0 import AzureIntegrationDefaultHeadersType0
        from ..models.azure_integration_extra_type_0 import AzureIntegrationExtraType0
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        endpoint = self.endpoint

        multi_modal_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.multi_modal_config, Unset):
            multi_modal_config = UNSET
        elif isinstance(self.multi_modal_config, MultiModalModelIntegrationConfig):
            multi_modal_config = self.multi_modal_config.to_dict()
        else:
            multi_modal_config = self.multi_modal_config

        proxy = self.proxy

        api_version = self.api_version

        azure_deployment: Union[None, Unset, str]
        azure_deployment = UNSET if isinstance(self.azure_deployment, Unset) else self.azure_deployment

        authentication_type: Union[Unset, str] = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value

        authentication_scope: Union[None, Unset, str]
        authentication_scope = UNSET if isinstance(self.authentication_scope, Unset) else self.authentication_scope

        default_headers: Union[None, Unset, dict[str, Any]]
        if isinstance(self.default_headers, Unset):
            default_headers = UNSET
        elif isinstance(self.default_headers, AzureIntegrationDefaultHeadersType0):
            default_headers = self.default_headers.to_dict()
        else:
            default_headers = self.default_headers

        deployments: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.deployments, Unset):
            deployments = self.deployments.to_dict()

        oauth2_token_url: Union[None, Unset, str]
        oauth2_token_url = UNSET if isinstance(self.oauth2_token_url, Unset) else self.oauth2_token_url

        custom_header_mapping: Union[None, Unset, dict[str, Any]]
        if isinstance(self.custom_header_mapping, Unset):
            custom_header_mapping = UNSET
        elif isinstance(self.custom_header_mapping, AzureIntegrationCustomHeaderMappingType0):
            custom_header_mapping = self.custom_header_mapping.to_dict()
        else:
            custom_header_mapping = self.custom_header_mapping

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

        id: Union[None, Unset, str]
        id = UNSET if isinstance(self.id, Unset) else self.id

        name = self.name

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, AzureIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"endpoint": endpoint})
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
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.azure_integration_custom_header_mapping_type_0 import AzureIntegrationCustomHeaderMappingType0
        from ..models.azure_integration_default_headers_type_0 import AzureIntegrationDefaultHeadersType0
        from ..models.azure_integration_deployments import AzureIntegrationDeployments
        from ..models.azure_integration_extra_type_0 import AzureIntegrationExtraType0
        from ..models.azure_model_deployment import AzureModelDeployment
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
                return MultiModalModelIntegrationConfig.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["MultiModalModelIntegrationConfig", None, Unset], data)

        multi_modal_config = _parse_multi_modal_config(d.pop("multi_modal_config", UNSET))

        proxy = d.pop("proxy", UNSET)

        api_version = d.pop("api_version", UNSET)

        def _parse_azure_deployment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        azure_deployment = _parse_azure_deployment(d.pop("azure_deployment", UNSET))

        _authentication_type = d.pop("authentication_type", UNSET)
        authentication_type: Union[Unset, AzureAuthenticationType]
        if isinstance(_authentication_type, Unset):
            authentication_type = UNSET
        else:
            authentication_type = AzureAuthenticationType(_authentication_type)

        def _parse_authentication_scope(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        authentication_scope = _parse_authentication_scope(d.pop("authentication_scope", UNSET))

        def _parse_default_headers(data: object) -> Union["AzureIntegrationDefaultHeadersType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AzureIntegrationDefaultHeadersType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AzureIntegrationDefaultHeadersType0", None, Unset], data)

        default_headers = _parse_default_headers(d.pop("default_headers", UNSET))

        _deployments = d.pop("deployments", UNSET)
        deployments: Union[Unset, AzureIntegrationDeployments]
        deployments = UNSET if isinstance(_deployments, Unset) else AzureIntegrationDeployments.from_dict(_deployments)

        def _parse_oauth2_token_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        oauth2_token_url = _parse_oauth2_token_url(d.pop("oauth2_token_url", UNSET))

        def _parse_custom_header_mapping(
            data: object,
        ) -> Union["AzureIntegrationCustomHeaderMappingType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AzureIntegrationCustomHeaderMappingType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AzureIntegrationCustomHeaderMappingType0", None, Unset], data)

        custom_header_mapping = _parse_custom_header_mapping(d.pop("custom_header_mapping", UNSET))

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

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        name = cast(Union[Literal["azure"], Unset], d.pop("name", UNSET))
        if name != "azure" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'azure', got '{name}'")

        def _parse_extra(data: object) -> Union["AzureIntegrationExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AzureIntegrationExtraType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AzureIntegrationExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        azure_integration = cls(
            endpoint=endpoint,
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
            id=id,
            name=name,
            extra=extra,
        )

        azure_integration.additional_properties = d
        return azure_integration

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
