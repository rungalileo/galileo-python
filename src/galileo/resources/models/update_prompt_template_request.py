from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.name import Name


T = TypeVar("T", bound="UpdatePromptTemplateRequest")


@_attrs_define
class UpdatePromptTemplateRequest:
    """
    Attributes:
        name (Union['Name', None, Unset, str]):
    """

    name: Union["Name", None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.name import Name

        name: Union[None, Unset, dict[str, Any], str]
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, Name):
            name = self.name.to_dict()
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.name import Name

        d = dict(src_dict)

        def _parse_name(data: object) -> Union["Name", None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                name_type_1 = Name.from_dict(data)

                return name_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Name", None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        update_prompt_template_request = cls(name=name)

        update_prompt_template_request.additional_properties = d
        return update_prompt_template_request

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
