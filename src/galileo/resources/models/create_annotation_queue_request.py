from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.name import Name


T = TypeVar("T", bound="CreateAnnotationQueueRequest")


@_attrs_define
class CreateAnnotationQueueRequest:
    """
    Attributes:
        name (Name): Global name class for handling unique naming across the application.
        description (None | str | Unset):
        annotator_emails (list[str] | Unset):
        copy_templates_from_queue_id (None | str | Unset): Optional ID of an existing annotation queue to copy templates
            from
    """

    name: Name
    description: None | str | Unset = UNSET
    annotator_emails: list[str] | Unset = UNSET
    copy_templates_from_queue_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        annotator_emails: list[str] | Unset = UNSET
        if not isinstance(self.annotator_emails, Unset):
            annotator_emails = self.annotator_emails

        copy_templates_from_queue_id: None | str | Unset
        if isinstance(self.copy_templates_from_queue_id, Unset):
            copy_templates_from_queue_id = UNSET
        else:
            copy_templates_from_queue_id = self.copy_templates_from_queue_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if description is not UNSET:
            field_dict["description"] = description
        if annotator_emails is not UNSET:
            field_dict["annotator_emails"] = annotator_emails
        if copy_templates_from_queue_id is not UNSET:
            field_dict["copy_templates_from_queue_id"] = copy_templates_from_queue_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.name import Name

        d = dict(src_dict)
        name = Name.from_dict(d.pop("name"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        annotator_emails = cast(list[str], d.pop("annotator_emails", UNSET))

        def _parse_copy_templates_from_queue_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        copy_templates_from_queue_id = _parse_copy_templates_from_queue_id(d.pop("copy_templates_from_queue_id", UNSET))

        create_annotation_queue_request = cls(
            name=name,
            description=description,
            annotator_emails=annotator_emails,
            copy_templates_from_queue_id=copy_templates_from_queue_id,
        )

        create_annotation_queue_request.additional_properties = d
        return create_annotation_queue_request

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
