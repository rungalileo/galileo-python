from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationModelsResponse")


@_attrs_define
class IntegrationModelsResponse:
    """
    Attributes
    ----------
        integration_name (str):
        models (list[str]):
        scorer_models (list[str]):
        supports_num_judges (Union[Unset, bool]):  Default: True.
    """

    integration_name: str
    models: list[str]
    scorer_models: list[str]
    supports_num_judges: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integration_name = self.integration_name

        models = self.models

        scorer_models = self.scorer_models

        supports_num_judges = self.supports_num_judges

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"integration_name": integration_name, "models": models, "scorer_models": scorer_models})
        if supports_num_judges is not UNSET:
            field_dict["supports_num_judges"] = supports_num_judges

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        integration_name = d.pop("integration_name")

        models = cast(list[str], d.pop("models"))

        scorer_models = cast(list[str], d.pop("scorer_models"))

        supports_num_judges = d.pop("supports_num_judges", UNSET)

        integration_models_response = cls(
            integration_name=integration_name,
            models=models,
            scorer_models=scorer_models,
            supports_num_judges=supports_num_judges,
        )

        integration_models_response.additional_properties = d
        return integration_models_response

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
