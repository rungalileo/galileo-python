from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomIntegrationModelProperties")


@_attrs_define
class CustomIntegrationModelProperties:
    """Properties for a model in a custom integration.

    Attributes:
        name: The model name used when calling the API.
        alias: The display name/alias for the model in the UI.
              Defaults to ``name`` when not provided.
        based_on: Alias of a built-in model whose parameter map should be used.
                  Mutually exclusive with ``supported_parameters``.
        supported_parameters: Explicit list of parameter names this model supports.
                              Mutually exclusive with ``based_on``.

        Attributes:
            name (str): The model name used when calling the API.
            alias (Union[None, Unset, str]): The display name/alias for the model. Defaults to name.
            based_on (Union[None, Unset, str]): Alias of a built-in model whose parameter map should be used. For example,
                'gpt-5.4'. Mutually exclusive with supported_parameters.
            supported_parameters (Union[None, Unset, list[str]]): Explicit list of parameter names this model supports
                (e.g., ['max_tokens', 'temperature', 'verbosity']). Each name must be a valid RunParamsMap field. Mutually
                exclusive with based_on.
    """

    name: str
    alias: Union[None, Unset, str] = UNSET
    based_on: Union[None, Unset, str] = UNSET
    supported_parameters: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        alias: Union[None, Unset, str]
        if isinstance(self.alias, Unset):
            alias = UNSET
        else:
            alias = self.alias

        based_on: Union[None, Unset, str]
        if isinstance(self.based_on, Unset):
            based_on = UNSET
        else:
            based_on = self.based_on

        supported_parameters: Union[None, Unset, list[str]]
        if isinstance(self.supported_parameters, Unset):
            supported_parameters = UNSET
        elif isinstance(self.supported_parameters, list):
            supported_parameters = self.supported_parameters

        else:
            supported_parameters = self.supported_parameters

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if alias is not UNSET:
            field_dict["alias"] = alias
        if based_on is not UNSET:
            field_dict["based_on"] = based_on
        if supported_parameters is not UNSET:
            field_dict["supported_parameters"] = supported_parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        alias = _parse_alias(d.pop("alias", UNSET))

        def _parse_based_on(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        based_on = _parse_based_on(d.pop("based_on", UNSET))

        def _parse_supported_parameters(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                supported_parameters_type_0 = cast(list[str], data)

                return supported_parameters_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        supported_parameters = _parse_supported_parameters(d.pop("supported_parameters", UNSET))

        custom_integration_model_properties = cls(
            name=name, alias=alias, based_on=based_on, supported_parameters=supported_parameters
        )

        custom_integration_model_properties.additional_properties = d
        return custom_integration_model_properties

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
