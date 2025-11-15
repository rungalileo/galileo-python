from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_authentication_type import CustomAuthenticationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomIntegrationCreate")


@_attrs_define
class CustomIntegrationCreate:
    """
    Attributes
    ----------
        endpoint (str): Endpoint URL for the custom integration.
        models (list[str]): List of model names for the custom integration
        token (str):
        authentication_scope (Union[None, Unset, str]): Optional scope for OAuth2 authentication.
        authentication_type (Union[Unset, CustomAuthenticationType]):
        default_model (Union[None, Unset, str]): Default model to use. If not provided, defaults to the first model in
            the models list.
        oauth2_token_url (Union[None, Unset, str]): OAuth2 token URL for custom OAuth2 authentication. If not provided,
            defaults to the endpoint.
    """

    endpoint: str
    models: list[str]
    token: str
    authentication_scope: Union[None, Unset, str] = UNSET
    authentication_type: Union[Unset, CustomAuthenticationType] = UNSET
    default_model: Union[None, Unset, str] = UNSET
    oauth2_token_url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        endpoint = self.endpoint

        models = self.models

        token = self.token

        authentication_scope: Union[None, Unset, str]
        authentication_scope = UNSET if isinstance(self.authentication_scope, Unset) else self.authentication_scope

        authentication_type: Union[Unset, str] = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value

        default_model: Union[None, Unset, str]
        default_model = UNSET if isinstance(self.default_model, Unset) else self.default_model

        oauth2_token_url: Union[None, Unset, str]
        oauth2_token_url = UNSET if isinstance(self.oauth2_token_url, Unset) else self.oauth2_token_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"endpoint": endpoint, "models": models, "token": token})
        if authentication_scope is not UNSET:
            field_dict["authentication_scope"] = authentication_scope
        if authentication_type is not UNSET:
            field_dict["authentication_type"] = authentication_type
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if oauth2_token_url is not UNSET:
            field_dict["oauth2_token_url"] = oauth2_token_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        models = cast(list[str], d.pop("models"))

        token = d.pop("token")

        def _parse_authentication_scope(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        authentication_scope = _parse_authentication_scope(d.pop("authentication_scope", UNSET))

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

        def _parse_oauth2_token_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        oauth2_token_url = _parse_oauth2_token_url(d.pop("oauth2_token_url", UNSET))

        custom_integration_create = cls(
            endpoint=endpoint,
            models=models,
            token=token,
            authentication_scope=authentication_scope,
            authentication_type=authentication_type,
            default_model=default_model,
            oauth2_token_url=oauth2_token_url,
        )

        custom_integration_create.additional_properties = d
        return custom_integration_create

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
