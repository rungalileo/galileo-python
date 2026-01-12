from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.aws_credential_type import AwsCredentialType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aws_bedrock_integration_extra_type_0 import AwsBedrockIntegrationExtraType0
    from ..models.aws_bedrock_integration_inference_profiles import AwsBedrockIntegrationInferenceProfiles


T = TypeVar("T", bound="AwsBedrockIntegration")


@_attrs_define
class AwsBedrockIntegration:
    """
    Attributes
    ----------
        credential_type (Union[Unset, AwsCredentialType]):
        region (Union[Unset, str]):  Default: 'us-west-2'.
        inference_profiles (Union[Unset, AwsBedrockIntegrationInferenceProfiles]): Mapping from model name (Foundation
            model ID) to inference profile ARN or ID
        id (Union[None, Unset, str]):
        name (Union[Literal['aws_bedrock'], Unset]):  Default: 'aws_bedrock'.
        extra (Union['AwsBedrockIntegrationExtraType0', None, Unset]):
    """

    credential_type: Union[Unset, AwsCredentialType] = UNSET
    region: Union[Unset, str] = "us-west-2"
    inference_profiles: Union[Unset, "AwsBedrockIntegrationInferenceProfiles"] = UNSET
    id: Union[None, Unset, str] = UNSET
    name: Union[Literal["aws_bedrock"], Unset] = "aws_bedrock"
    extra: Union["AwsBedrockIntegrationExtraType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.aws_bedrock_integration_extra_type_0 import AwsBedrockIntegrationExtraType0

        credential_type: Union[Unset, str] = UNSET
        if not isinstance(self.credential_type, Unset):
            credential_type = self.credential_type.value

        region = self.region

        inference_profiles: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.inference_profiles, Unset):
            inference_profiles = self.inference_profiles.to_dict()

        id: Union[None, Unset, str]
        id = UNSET if isinstance(self.id, Unset) else self.id

        name = self.name

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, AwsBedrockIntegrationExtraType0):
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
        if inference_profiles is not UNSET:
            field_dict["inference_profiles"] = inference_profiles
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aws_bedrock_integration_extra_type_0 import AwsBedrockIntegrationExtraType0
        from ..models.aws_bedrock_integration_inference_profiles import AwsBedrockIntegrationInferenceProfiles

        d = dict(src_dict)
        _credential_type = d.pop("credential_type", UNSET)
        credential_type: Union[Unset, AwsCredentialType]
        credential_type = UNSET if isinstance(_credential_type, Unset) else AwsCredentialType(_credential_type)

        region = d.pop("region", UNSET)

        _inference_profiles = d.pop("inference_profiles", UNSET)
        inference_profiles: Union[Unset, AwsBedrockIntegrationInferenceProfiles]
        if isinstance(_inference_profiles, Unset):
            inference_profiles = UNSET
        else:
            inference_profiles = AwsBedrockIntegrationInferenceProfiles.from_dict(_inference_profiles)

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        name = cast(Union[Literal["aws_bedrock"], Unset], d.pop("name", UNSET))
        if name != "aws_bedrock" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'aws_bedrock', got '{name}'")

        def _parse_extra(data: object) -> Union["AwsBedrockIntegrationExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AwsBedrockIntegrationExtraType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AwsBedrockIntegrationExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        aws_bedrock_integration = cls(
            credential_type=credential_type,
            region=region,
            inference_profiles=inference_profiles,
            id=id,
            name=name,
            extra=extra,
        )

        aws_bedrock_integration.additional_properties = d
        return aws_bedrock_integration

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
