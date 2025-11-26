import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.project_labels import ProjectLabels
from ..models.project_type import ProjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectUpdateResponse")


@_attrs_define
class ProjectUpdateResponse:
    """
    Attributes
    ----------
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        name (Union[None, Unset, str]):
        created_by (Union[None, Unset, str]):
        type_ (Union[None, ProjectType, Unset]):
        labels (Union[Unset, list[ProjectLabels]]):
        description (Union[None, Unset, str]):
    """

    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: Union[None, Unset, str] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    type_: Union[None, ProjectType, Unset] = UNSET
    labels: Union[Unset, list[ProjectLabels]] = UNSET
    description: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        name: Union[None, Unset, str]
        name = UNSET if isinstance(self.name, Unset) else self.name

        created_by: Union[None, Unset, str]
        created_by = UNSET if isinstance(self.created_by, Unset) else self.created_by

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, ProjectType):
            type_ = self.type_.value
        else:
            type_ = self.type_

        labels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = []
            for labels_item_data in self.labels:
                labels_item = labels_item_data.value
                labels.append(labels_item)

        description: Union[None, Unset, str]
        description = UNSET if isinstance(self.description, Unset) else self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "created_at": created_at, "updated_at": updated_at})
        if name is not UNSET:
            field_dict["name"] = name
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if type_ is not UNSET:
            field_dict["type"] = type_
        if labels is not UNSET:
            field_dict["labels"] = labels
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_type_(data: object) -> Union[None, ProjectType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ProjectType(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, ProjectType, Unset], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        labels = []
        _labels = d.pop("labels", UNSET)
        for labels_item_data in _labels or []:
            labels_item = ProjectLabels(labels_item_data)

            labels.append(labels_item)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        project_update_response = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            created_by=created_by,
            type_=type_,
            labels=labels,
            description=description,
        )

        project_update_response.additional_properties = d
        return project_update_response

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
