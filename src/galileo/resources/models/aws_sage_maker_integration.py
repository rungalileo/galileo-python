from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.aws_credential_type import AwsCredentialType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aws_sage_maker_integration_extra_type_0 import AwsSageMakerIntegrationExtraType0
    from ..models.model import Model
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig


T = TypeVar("T", bound="AwsSageMakerIntegration")


@_attrs_define
class AwsSageMakerIntegration:
    """
    Attributes:
        credential_type (AwsCredentialType | Unset):
        region (str | Unset):  Default: 'us-west-2'.
        multi_modal_config (MultiModalModelIntegrationConfig | None | Unset): Configuration for multi-modal (file
            upload) capabilities.
        models (list[Model] | Unset):
        id (None | str | Unset):
        name (Literal['aws_sagemaker'] | Unset):  Default: 'aws_sagemaker'.
        extra (AwsSageMakerIntegrationExtraType0 | None | Unset):
    """

    credential_type: AwsCredentialType | Unset = UNSET
    region: str | Unset = "us-west-2"
    multi_modal_config: MultiModalModelIntegrationConfig | None | Unset = UNSET
    models: list[Model] | Unset = UNSET
    id: None | str | Unset = UNSET
    name: Literal["aws_sagemaker"] | Unset = "aws_sagemaker"
    extra: AwsSageMakerIntegrationExtraType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.aws_sage_maker_integration_extra_type_0 import AwsSageMakerIntegrationExtraType0
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        credential_type: str | Unset = UNSET
        if not isinstance(self.credential_type, Unset):
            credential_type = self.credential_type.value

        region = self.region

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

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name = self.name

        extra: dict[str, Any] | None | Unset
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, AwsSageMakerIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if credential_type is not UNSET:
            field_dict["credential_type"] = credential_type
        if region is not UNSET:
            field_dict["region"] = region
        if multi_modal_config is not UNSET:
            field_dict["multi_modal_config"] = multi_modal_config
        if models is not UNSET:
            field_dict["models"] = models
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aws_sage_maker_integration_extra_type_0 import AwsSageMakerIntegrationExtraType0
        from ..models.model import Model
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig

        d = dict(src_dict)
        _credential_type = d.pop("credential_type", UNSET)
        credential_type: AwsCredentialType | Unset
        if isinstance(_credential_type, Unset):
            credential_type = UNSET
        else:
            credential_type = AwsCredentialType(_credential_type)

        region = d.pop("region", UNSET)

        def _parse_multi_modal_config(data: object) -> MultiModalModelIntegrationConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                multi_modal_config_type_0 = MultiModalModelIntegrationConfig.from_dict(data)

                return multi_modal_config_type_0
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

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        name = cast(Literal["aws_sagemaker"] | Unset, d.pop("name", UNSET))
        if name != "aws_sagemaker" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'aws_sagemaker', got '{name}'")

        def _parse_extra(data: object) -> AwsSageMakerIntegrationExtraType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = AwsSageMakerIntegrationExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(AwsSageMakerIntegrationExtraType0 | None | Unset, data)

        extra = _parse_extra(d.pop("extra", UNSET))

        aws_sage_maker_integration = cls(
            credential_type=credential_type,
            region=region,
            multi_modal_config=multi_modal_config,
            models=models,
            id=id,
            name=name,
            extra=extra,
        )

        aws_sage_maker_integration.additional_properties = d
        return aws_sage_maker_integration

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
