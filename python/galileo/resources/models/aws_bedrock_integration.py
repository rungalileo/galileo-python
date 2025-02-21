from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.aws_credential_type import AwsCredentialType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aws_bedrock_integration_extra_type_0 import AwsBedrockIntegrationExtraType0


T = TypeVar("T", bound="AwsBedrockIntegration")


@_attrs_define
class AwsBedrockIntegration:
    """
    Attributes:
        credential_type (Union[Unset, AwsCredentialType]):
        extra (Union['AwsBedrockIntegrationExtraType0', None, Unset]):
        name (Union[Literal['aws_bedrock'], Unset]):  Default: 'aws_bedrock'.
        region (Union[Unset, str]):  Default: 'us-west-2'.
    """

    credential_type: Union[Unset, AwsCredentialType] = UNSET
    extra: Union["AwsBedrockIntegrationExtraType0", None, Unset] = UNSET
    name: Union[Literal["aws_bedrock"], Unset] = "aws_bedrock"
    region: Union[Unset, str] = "us-west-2"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.aws_bedrock_integration_extra_type_0 import AwsBedrockIntegrationExtraType0

        credential_type: Union[Unset, str] = UNSET
        if not isinstance(self.credential_type, Unset):
            credential_type = self.credential_type.value

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, AwsBedrockIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        name = self.name

        region = self.region

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if credential_type is not UNSET:
            field_dict["credential_type"] = credential_type
        if extra is not UNSET:
            field_dict["extra"] = extra
        if name is not UNSET:
            field_dict["name"] = name
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aws_bedrock_integration_extra_type_0 import AwsBedrockIntegrationExtraType0

        d = src_dict.copy()
        _credential_type = d.pop("credential_type", UNSET)
        credential_type: Union[Unset, AwsCredentialType]
        if isinstance(_credential_type, Unset):
            credential_type = UNSET
        else:
            credential_type = AwsCredentialType(_credential_type)

        def _parse_extra(data: object) -> Union["AwsBedrockIntegrationExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = AwsBedrockIntegrationExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AwsBedrockIntegrationExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        name = cast(Union[Literal["aws_bedrock"], Unset], d.pop("name", UNSET))
        if name != "aws_bedrock" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'aws_bedrock', got '{name}'")

        region = d.pop("region", UNSET)

        aws_bedrock_integration = cls(credential_type=credential_type, extra=extra, name=name, region=region)

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
