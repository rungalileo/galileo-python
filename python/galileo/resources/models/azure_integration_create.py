from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.azure_authentication_type import AzureAuthenticationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.azure_integration_create_headers_type_0 import AzureIntegrationCreateHeadersType0
    from ..models.azure_model_deployment import AzureModelDeployment


T = TypeVar("T", bound="AzureIntegrationCreate")


@_attrs_define
class AzureIntegrationCreate:
    """
    Attributes:
        endpoint (str):
        token (str):
        api_version (Union[Unset, str]):  Default: '2024-10-21'.
        authentication_scope (Union[None, Unset, str]):
        authentication_type (Union[Unset, AzureAuthenticationType]):
        available_deployments (Union[None, Unset, list['AzureModelDeployment']]): The available deployments for this
            integration. If provided, we will not try to get this list from Azure.
        azure_deployment (Union[None, Unset, str]):
        headers (Union['AzureIntegrationCreateHeadersType0', None, Unset]):
        proxy (Union[Unset, bool]):  Default: False.
    """

    endpoint: str
    token: str
    api_version: Union[Unset, str] = "2024-10-21"
    authentication_scope: Union[None, Unset, str] = UNSET
    authentication_type: Union[Unset, AzureAuthenticationType] = UNSET
    available_deployments: Union[None, Unset, list["AzureModelDeployment"]] = UNSET
    azure_deployment: Union[None, Unset, str] = UNSET
    headers: Union["AzureIntegrationCreateHeadersType0", None, Unset] = UNSET
    proxy: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.azure_integration_create_headers_type_0 import AzureIntegrationCreateHeadersType0

        endpoint = self.endpoint

        token = self.token

        api_version = self.api_version

        authentication_scope: Union[None, Unset, str]
        if isinstance(self.authentication_scope, Unset):
            authentication_scope = UNSET
        else:
            authentication_scope = self.authentication_scope

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
        if isinstance(self.azure_deployment, Unset):
            azure_deployment = UNSET
        else:
            azure_deployment = self.azure_deployment

        headers: Union[None, Unset, dict[str, Any]]
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, AzureIntegrationCreateHeadersType0):
            headers = self.headers.to_dict()
        else:
            headers = self.headers

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
        if headers is not UNSET:
            field_dict["headers"] = headers
        if proxy is not UNSET:
            field_dict["proxy"] = proxy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.azure_integration_create_headers_type_0 import AzureIntegrationCreateHeadersType0
        from ..models.azure_model_deployment import AzureModelDeployment

        d = src_dict.copy()
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

        def _parse_headers(data: object) -> Union["AzureIntegrationCreateHeadersType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                headers_type_0 = AzureIntegrationCreateHeadersType0.from_dict(data)

                return headers_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AzureIntegrationCreateHeadersType0", None, Unset], data)

        headers = _parse_headers(d.pop("headers", UNSET))

        proxy = d.pop("proxy", UNSET)

        azure_integration_create = cls(
            endpoint=endpoint,
            token=token,
            api_version=api_version,
            authentication_scope=authentication_scope,
            authentication_type=authentication_type,
            available_deployments=available_deployments,
            azure_deployment=azure_deployment,
            headers=headers,
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
