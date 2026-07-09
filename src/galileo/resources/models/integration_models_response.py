from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_models_response_recommended_models import IntegrationModelsResponseRecommendedModels
    from ..models.model_properties import ModelProperties


T = TypeVar("T", bound="IntegrationModelsResponse")


@_attrs_define
class IntegrationModelsResponse:
    """
    Attributes:
        integration_name (str):
        models (list[str]):
        scorer_models (list[str]):
        recommended_models (IntegrationModelsResponseRecommendedModels | Unset):
        supports_num_judges (bool | Unset):  Default: True.
        supports_file_uploads (bool | Unset):  Default: False.
        model_properties (list[ModelProperties] | Unset):
    """

    integration_name: str
    models: list[str]
    scorer_models: list[str]
    recommended_models: IntegrationModelsResponseRecommendedModels | Unset = UNSET
    supports_num_judges: bool | Unset = True
    supports_file_uploads: bool | Unset = False
    model_properties: list[ModelProperties] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integration_name = self.integration_name

        models = self.models

        scorer_models = self.scorer_models

        recommended_models: dict[str, Any] | Unset = UNSET
        if not isinstance(self.recommended_models, Unset):
            recommended_models = self.recommended_models.to_dict()

        supports_num_judges = self.supports_num_judges

        supports_file_uploads = self.supports_file_uploads

        model_properties: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.model_properties, Unset):
            model_properties = []
            for model_properties_item_data in self.model_properties:
                model_properties_item = model_properties_item_data.to_dict()
                model_properties.append(model_properties_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"integration_name": integration_name, "models": models, "scorer_models": scorer_models})
        if recommended_models is not UNSET:
            field_dict["recommended_models"] = recommended_models
        if supports_num_judges is not UNSET:
            field_dict["supports_num_judges"] = supports_num_judges
        if supports_file_uploads is not UNSET:
            field_dict["supports_file_uploads"] = supports_file_uploads
        if model_properties is not UNSET:
            field_dict["model_properties"] = model_properties

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_models_response_recommended_models import IntegrationModelsResponseRecommendedModels
        from ..models.model_properties import ModelProperties

        d = dict(src_dict)
        integration_name = d.pop("integration_name")

        models = cast(list[str], d.pop("models"))

        scorer_models = cast(list[str], d.pop("scorer_models"))

        _recommended_models = d.pop("recommended_models", UNSET)
        recommended_models: IntegrationModelsResponseRecommendedModels | Unset
        if isinstance(_recommended_models, Unset):
            recommended_models = UNSET
        else:
            recommended_models = IntegrationModelsResponseRecommendedModels.from_dict(_recommended_models)

        supports_num_judges = d.pop("supports_num_judges", UNSET)

        supports_file_uploads = d.pop("supports_file_uploads", UNSET)

        _model_properties = d.pop("model_properties", UNSET)
        model_properties: list[ModelProperties] | Unset = UNSET
        if _model_properties is not UNSET:
            model_properties = []
            for model_properties_item_data in _model_properties:
                model_properties_item = ModelProperties.from_dict(model_properties_item_data)

                model_properties.append(model_properties_item)

        integration_models_response = cls(
            integration_name=integration_name,
            models=models,
            scorer_models=scorer_models,
            recommended_models=recommended_models,
            supports_num_judges=supports_num_judges,
            supports_file_uploads=supports_file_uploads,
            model_properties=model_properties,
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
