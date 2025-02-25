from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptGroupResponse")


@_attrs_define
class PromptGroupResponse:
    """Contains relevant data for prompt column group.

    Attributes:
        columns (list[str]):
        group_label (str):
        group_description (Union[None, Unset, str]):
        group_icon (Union[Unset, str]):  Default: 'Puzzle'.
        group_name (Union[None, Unset, str]):
    """

    columns: list[str]
    group_label: str
    group_description: Union[None, Unset, str] = UNSET
    group_icon: Union[Unset, str] = "Puzzle"
    group_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        columns = self.columns

        group_label = self.group_label

        group_description: Union[None, Unset, str]
        if isinstance(self.group_description, Unset):
            group_description = UNSET
        else:
            group_description = self.group_description

        group_icon = self.group_icon

        group_name: Union[None, Unset, str]
        if isinstance(self.group_name, Unset):
            group_name = UNSET
        else:
            group_name = self.group_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"columns": columns, "group_label": group_label})
        if group_description is not UNSET:
            field_dict["group_description"] = group_description
        if group_icon is not UNSET:
            field_dict["group_icon"] = group_icon
        if group_name is not UNSET:
            field_dict["group_name"] = group_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        columns = cast(list[str], d.pop("columns"))

        group_label = d.pop("group_label")

        def _parse_group_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_description = _parse_group_description(d.pop("group_description", UNSET))

        group_icon = d.pop("group_icon", UNSET)

        def _parse_group_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_name = _parse_group_name(d.pop("group_name", UNSET))

        prompt_group_response = cls(
            columns=columns,
            group_label=group_label,
            group_description=group_description,
            group_icon=group_icon,
            group_name=group_name,
        )

        prompt_group_response.additional_properties = d
        return prompt_group_response

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
