from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_prompt_template_version_response import BasePromptTemplateVersionResponse


T = TypeVar("T", bound="BasePromptTemplateResponse")


@_attrs_define
class BasePromptTemplateResponse:
    """Response from API to get a prompt template version.

    Attributes:
        all_available_versions (list[int]):
        id (str):
        max_version (int):
        name (str):
        selected_version (BasePromptTemplateVersionResponse): Base response from API for a prompt template version.
        selected_version_id (str):
        template (str):
        total_versions (int):
        all_versions (Union[Unset, list['BasePromptTemplateVersionResponse']]):
    """

    all_available_versions: list[int]
    id: str
    max_version: int
    name: str
    selected_version: "BasePromptTemplateVersionResponse"
    selected_version_id: str
    template: str
    total_versions: int
    all_versions: Union[Unset, list["BasePromptTemplateVersionResponse"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        all_available_versions = self.all_available_versions

        id = self.id

        max_version = self.max_version

        name = self.name

        selected_version = self.selected_version.to_dict()

        selected_version_id = self.selected_version_id

        template = self.template

        total_versions = self.total_versions

        all_versions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.all_versions, Unset):
            all_versions = []
            for all_versions_item_data in self.all_versions:
                all_versions_item = all_versions_item_data.to_dict()
                all_versions.append(all_versions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "all_available_versions": all_available_versions,
                "id": id,
                "max_version": max_version,
                "name": name,
                "selected_version": selected_version,
                "selected_version_id": selected_version_id,
                "template": template,
                "total_versions": total_versions,
            }
        )
        if all_versions is not UNSET:
            field_dict["all_versions"] = all_versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.base_prompt_template_version_response import BasePromptTemplateVersionResponse

        d = src_dict.copy()
        all_available_versions = cast(list[int], d.pop("all_available_versions"))

        id = d.pop("id")

        max_version = d.pop("max_version")

        name = d.pop("name")

        selected_version = BasePromptTemplateVersionResponse.from_dict(d.pop("selected_version"))

        selected_version_id = d.pop("selected_version_id")

        template = d.pop("template")

        total_versions = d.pop("total_versions")

        all_versions = []
        _all_versions = d.pop("all_versions", UNSET)
        for all_versions_item_data in _all_versions or []:
            all_versions_item = BasePromptTemplateVersionResponse.from_dict(all_versions_item_data)

            all_versions.append(all_versions_item)

        base_prompt_template_response = cls(
            all_available_versions=all_available_versions,
            id=id,
            max_version=max_version,
            name=name,
            selected_version=selected_version,
            selected_version_id=selected_version_id,
            template=template,
            total_versions=total_versions,
            all_versions=all_versions,
        )

        base_prompt_template_response.additional_properties = d
        return base_prompt_template_response

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
