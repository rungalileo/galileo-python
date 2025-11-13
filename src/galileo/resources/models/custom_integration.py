from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_authentication_type import CustomAuthenticationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0


T = TypeVar("T", bound="CustomIntegration")


@_attrs_define
class CustomIntegration:
    """
    Attributes
    ----------
        endpoint (str): Endpoint URL for the custom integration.
        models (list[str]): List of model names for the custom integration
        authentication_scope (Union[None, Unset, str]): Optional scope for OAuth2 authentication.
        authentication_type (Union[Unset, CustomAuthenticationType]):
        default_model (Union[None, Unset, str]): Default model to use. If not provided, defaults to the first model in
            the models list.
        extra (Union['CustomIntegrationExtraType0', None, Unset]):
        id (Union[None, Unset, str]):
        name (Union[Literal['custom'], Unset]):  Default: 'custom'.
        oauth2_token_url (Union[None, Unset, str]): OAuth2 token URL for custom OAuth2 authentication. If not provided,
            defaults to the endpoint.
    """

    endpoint: str
    models: list[str]
    authentication_scope: Union[None, Unset, str] = UNSET
    authentication_type: Union[Unset, CustomAuthenticationType] = UNSET
    default_model: Union[None, Unset, str] = UNSET
    extra: Union["CustomIntegrationExtraType0", None, Unset] = UNSET
    id: Union[None, Unset, str] = UNSET
    name: Union[Literal["custom"], Unset] = "custom"
    oauth2_token_url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0

        endpoint = self.endpoint

        models = self.models

        authentication_scope: Union[None, Unset, str]
        authentication_scope = UNSET if isinstance(self.authentication_scope, Unset) else self.authentication_scope

        authentication_type: Union[Unset, str] = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type.value

        default_model: Union[None, Unset, str]
        default_model = UNSET if isinstance(self.default_model, Unset) else self.default_model

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, CustomIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        id: Union[None, Unset, str]
        id = UNSET if isinstance(self.id, Unset) else self.id

        name = self.name

        oauth2_token_url: Union[None, Unset, str]
        oauth2_token_url = UNSET if isinstance(self.oauth2_token_url, Unset) else self.oauth2_token_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"endpoint": endpoint, "models": models})
        if authentication_scope is not UNSET:
            field_dict["authentication_scope"] = authentication_scope
        if authentication_type is not UNSET:
            field_dict["authentication_type"] = authentication_type
        if default_model is not UNSET:
            field_dict["default_model"] = default_model
        if extra is not UNSET:
            field_dict["extra"] = extra
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if oauth2_token_url is not UNSET:
            field_dict["oauth2_token_url"] = oauth2_token_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_integration_extra_type_0 import CustomIntegrationExtraType0

        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        models = cast(list[str], d.pop("models"))

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

        def _parse_oauth2_token_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        oauth2_token_url = _parse_oauth2_token_url(d.pop("oauth2_token_url", UNSET))

        custom_integration = cls(
            endpoint=endpoint,
            models=models,
            authentication_scope=authentication_scope,
            authentication_type=authentication_type,
            default_model=default_model,
            extra=extra,
            id=id,
            name=name,
            oauth2_token_url=oauth2_token_url,
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
