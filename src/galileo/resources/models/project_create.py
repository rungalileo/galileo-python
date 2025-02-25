from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_type import ProjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectCreate")


@_attrs_define
class ProjectCreate:
    """
    Attributes:
        name (str):
        create_example_templates (Union[Unset, bool]):  Default: False.
        created_by (Union[None, Unset, str]):
        type_ (Union[Unset, ProjectType]):
    """

    name: str
    create_example_templates: Union[Unset, bool] = False
    created_by: Union[None, Unset, str] = UNSET
    type_: Union[Unset, ProjectType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        create_example_templates = self.create_example_templates

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if create_example_templates is not UNSET:
            field_dict["create_example_templates"] = create_example_templates
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        create_example_templates = d.pop("create_example_templates", UNSET)

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, ProjectType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ProjectType(_type_)

        project_create = cls(
            name=name, create_example_templates=create_example_templates, created_by=created_by, type_=type_
        )

        project_create.additional_properties = d
        return project_create

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
