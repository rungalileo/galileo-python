from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.aws_credential_type import AwsCredentialType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aws_sage_maker_integration_extra_type_0 import AwsSageMakerIntegrationExtraType0
    from ..models.model import Model


T = TypeVar("T", bound="AwsSageMakerIntegration")


@_attrs_define
class AwsSageMakerIntegration:
    """
    Attributes:
        credential_type (Union[Unset, AwsCredentialType]):
        extra (Union['AwsSageMakerIntegrationExtraType0', None, Unset]):
        models (Union[Unset, list['Model']]):
        name (Union[Literal['aws_sagemaker'], Unset]):  Default: 'aws_sagemaker'.
        region (Union[Unset, str]):  Default: 'us-west-2'.
    """

    credential_type: Union[Unset, AwsCredentialType] = UNSET
    extra: Union["AwsSageMakerIntegrationExtraType0", None, Unset] = UNSET
    models: Union[Unset, list["Model"]] = UNSET
    name: Union[Literal["aws_sagemaker"], Unset] = "aws_sagemaker"
    region: Union[Unset, str] = "us-west-2"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.aws_sage_maker_integration_extra_type_0 import AwsSageMakerIntegrationExtraType0

        credential_type: Union[Unset, str] = UNSET
        if not isinstance(self.credential_type, Unset):
            credential_type = self.credential_type.value

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, AwsSageMakerIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        models: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.models, Unset):
            models = []
            for models_item_data in self.models:
                models_item = models_item_data.to_dict()
                models.append(models_item)

        name = self.name

        region = self.region

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if credential_type is not UNSET:
            field_dict["credential_type"] = credential_type
        if extra is not UNSET:
            field_dict["extra"] = extra
        if models is not UNSET:
            field_dict["models"] = models
        if name is not UNSET:
            field_dict["name"] = name
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aws_sage_maker_integration_extra_type_0 import AwsSageMakerIntegrationExtraType0
        from ..models.model import Model

        d = src_dict.copy()
        _credential_type = d.pop("credential_type", UNSET)
        credential_type: Union[Unset, AwsCredentialType]
        if isinstance(_credential_type, Unset):
            credential_type = UNSET
        else:
            credential_type = AwsCredentialType(_credential_type)

        def _parse_extra(data: object) -> Union["AwsSageMakerIntegrationExtraType0", None, Unset]:
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
            return cast(Union["AwsSageMakerIntegrationExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        models = []
        _models = d.pop("models", UNSET)
        for models_item_data in _models or []:
            models_item = Model.from_dict(models_item_data)

            models.append(models_item)

        name = cast(Union[Literal["aws_sagemaker"], Unset], d.pop("name", UNSET))
        if name != "aws_sagemaker" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'aws_sagemaker', got '{name}'")

        region = d.pop("region", UNSET)

        aws_sage_maker_integration = cls(
            credential_type=credential_type, extra=extra, models=models, name=name, region=region
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
