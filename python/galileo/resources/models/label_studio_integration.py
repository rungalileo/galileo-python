from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.label_studio_integration_extra_type_0 import LabelStudioIntegrationExtraType0


T = TypeVar("T", bound="LabelStudioIntegration")


@_attrs_define
class LabelStudioIntegration:
    """The active labelstudio integration information.

    Attributes:
        is_enterprise (bool):
        url (str):
        extra (Union['LabelStudioIntegrationExtraType0', None, Unset]):
        name (Union[Literal['labelstudio'], Unset]):  Default: 'labelstudio'.
    """

    is_enterprise: bool
    url: str
    extra: Union["LabelStudioIntegrationExtraType0", None, Unset] = UNSET
    name: Union[Literal["labelstudio"], Unset] = "labelstudio"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.label_studio_integration_extra_type_0 import LabelStudioIntegrationExtraType0

        is_enterprise = self.is_enterprise

        url = self.url

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, LabelStudioIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"is_enterprise": is_enterprise, "url": url})
        if extra is not UNSET:
            field_dict["extra"] = extra
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.label_studio_integration_extra_type_0 import LabelStudioIntegrationExtraType0

        d = src_dict.copy()
        is_enterprise = d.pop("is_enterprise")

        url = d.pop("url")

        def _parse_extra(data: object) -> Union["LabelStudioIntegrationExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = LabelStudioIntegrationExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LabelStudioIntegrationExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        name = cast(Union[Literal["labelstudio"], Unset], d.pop("name", UNSET))
        if name != "labelstudio" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'labelstudio', got '{name}'")

        label_studio_integration = cls(is_enterprise=is_enterprise, url=url, extra=extra, name=name)

        label_studio_integration.additional_properties = d
        return label_studio_integration

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
