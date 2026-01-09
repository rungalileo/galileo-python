from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.aws_credential_type import AwsCredentialType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_aws_integration_create_inference_profiles import BaseAwsIntegrationCreateInferenceProfiles
    from ..models.base_aws_integration_create_token import BaseAwsIntegrationCreateToken


T = TypeVar("T", bound="BaseAwsIntegrationCreate")


@_attrs_define
class BaseAwsIntegrationCreate:
    """
    Attributes
    ----------
        token (BaseAwsIntegrationCreateToken):
        credential_type (Union[Unset, AwsCredentialType]):
        region (Union[Unset, str]):  Default: 'us-west-2'.
        inference_profiles (Union[Unset, BaseAwsIntegrationCreateInferenceProfiles]): Mapping from model name
            (Foundation model ID) to inference profile ARN or ID.
    """

    token: "BaseAwsIntegrationCreateToken"
    credential_type: Union[Unset, AwsCredentialType] = UNSET
    region: Union[Unset, str] = "us-west-2"
    inference_profiles: Union[Unset, "BaseAwsIntegrationCreateInferenceProfiles"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token.to_dict()

        credential_type: Union[Unset, str] = UNSET
        if not isinstance(self.credential_type, Unset):
            credential_type = self.credential_type.value

        region = self.region

        inference_profiles: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.inference_profiles, Unset):
            inference_profiles = self.inference_profiles.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"token": token})
        if credential_type is not UNSET:
            field_dict["credential_type"] = credential_type
        if region is not UNSET:
            field_dict["region"] = region
        if inference_profiles is not UNSET:
            field_dict["inference_profiles"] = inference_profiles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_aws_integration_create_inference_profiles import BaseAwsIntegrationCreateInferenceProfiles
        from ..models.base_aws_integration_create_token import BaseAwsIntegrationCreateToken

        d = dict(src_dict)
        token = BaseAwsIntegrationCreateToken.from_dict(d.pop("token"))

        _credential_type = d.pop("credential_type", UNSET)
        credential_type: Union[Unset, AwsCredentialType]
        credential_type = UNSET if isinstance(_credential_type, Unset) else AwsCredentialType(_credential_type)

        region = d.pop("region", UNSET)

        _inference_profiles = d.pop("inference_profiles", UNSET)
        inference_profiles: Union[Unset, BaseAwsIntegrationCreateInferenceProfiles]
        if isinstance(_inference_profiles, Unset):
            inference_profiles = UNSET
        else:
            inference_profiles = BaseAwsIntegrationCreateInferenceProfiles.from_dict(_inference_profiles)

        base_aws_integration_create = cls(
            token=token, credential_type=credential_type, region=region, inference_profiles=inference_profiles
        )

        base_aws_integration_create.additional_properties = d
        return base_aws_integration_create

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
