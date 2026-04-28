from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.aws_credential_type import AwsCredentialType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aws_sage_maker_integration_create_inference_profiles import (
        AwsSageMakerIntegrationCreateInferenceProfiles,
    )
    from ..models.aws_sage_maker_integration_create_token import AwsSageMakerIntegrationCreateToken
    from ..models.model import Model
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig


T = TypeVar("T", bound="AwsSageMakerIntegrationCreate")


@_attrs_define
class AwsSageMakerIntegrationCreate:
    """
    Attributes
    ----------
        token (AwsSageMakerIntegrationCreateToken):
        multi_modal_config (MultiModalModelIntegrationConfig | None | Unset): Configuration for multi-modal (file
            upload) capabilities.
        models (list[Model] | Unset):
        credential_type (AwsCredentialType | Unset):
        region (str | Unset):  Default: 'us-west-2'.
        inference_profiles (AwsSageMakerIntegrationCreateInferenceProfiles | Unset): Mapping from model name (Foundation
            model ID) to inference profile ARN or ID.
    """

    token: AwsSageMakerIntegrationCreateToken
    multi_modal_config: MultiModalModelIntegrationConfig | None | Unset = UNSET
    models: list[Model] | Unset = UNSET
    credential_type: AwsCredentialType | Unset = UNSET
    region: str | Unset = "us-west-2"
    inference_profiles: AwsSageMakerIntegrationCreateInferenceProfiles | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        token = self.token.to_dict()

        multi_modal_config: dict[str, Any] | None | Unset
        if isinstance(self.multi_modal_config, Unset):
            multi_modal_config = UNSET
        elif isinstance(self.multi_modal_config, MultiModalModelIntegrationConfig):
            multi_modal_config = self.multi_modal_config.to_dict()
        else:
            multi_modal_config = self.multi_modal_config

        models: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.models, Unset):
            models = []
            for models_item_data in self.models:
                models_item = models_item_data.to_dict()
                models.append(models_item)

        credential_type: str | Unset = UNSET
        if not isinstance(self.credential_type, Unset):
            credential_type = self.credential_type.value

        region = self.region

        inference_profiles: dict[str, Any] | Unset = UNSET
        if not isinstance(self.inference_profiles, Unset):
            inference_profiles = self.inference_profiles.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"token": token})
        if multi_modal_config is not UNSET:
            field_dict["multi_modal_config"] = multi_modal_config
        if models is not UNSET:
            field_dict["models"] = models
        if credential_type is not UNSET:
            field_dict["credential_type"] = credential_type
        if region is not UNSET:
            field_dict["region"] = region
        if inference_profiles is not UNSET:
            field_dict["inference_profiles"] = inference_profiles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aws_sage_maker_integration_create_inference_profiles import (
            AwsSageMakerIntegrationCreateInferenceProfiles,
        )
        from ..models.aws_sage_maker_integration_create_token import AwsSageMakerIntegrationCreateToken
        from ..models.model import Model
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        d = dict(src_dict)
        token = AwsSageMakerIntegrationCreateToken.from_dict(d.pop("token"))

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

        _models = d.pop("models", UNSET)
        models: list[Model] | Unset = UNSET
        if _models is not UNSET:
            models = []
            for models_item_data in _models:
                models_item = Model.from_dict(models_item_data)

                models.append(models_item)

        _credential_type = d.pop("credential_type", UNSET)
        credential_type: AwsCredentialType | Unset
        credential_type = UNSET if isinstance(_credential_type, Unset) else AwsCredentialType(_credential_type)

        region = d.pop("region", UNSET)

        _inference_profiles = d.pop("inference_profiles", UNSET)
        inference_profiles: AwsSageMakerIntegrationCreateInferenceProfiles | Unset
        if isinstance(_inference_profiles, Unset):
            inference_profiles = UNSET
        else:
            inference_profiles = AwsSageMakerIntegrationCreateInferenceProfiles.from_dict(_inference_profiles)

        aws_sage_maker_integration_create = cls(
            token=token,
            multi_modal_config=multi_modal_config,
            models=models,
            credential_type=credential_type,
            region=region,
            inference_profiles=inference_profiles,
        )

        aws_sage_maker_integration_create.additional_properties = d
        return aws_sage_maker_integration_create

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
