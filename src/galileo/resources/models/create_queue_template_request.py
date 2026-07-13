from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_template_create import AnnotationTemplateCreate


T = TypeVar("T", bound="CreateQueueTemplateRequest")


@_attrs_define
class CreateQueueTemplateRequest:
    """Request to create templates in an annotation queue.

    Supports two scenarios:
    1. Create a single template (template field)
    2. Copy all templates from a source queue (copy_from_queue_id field)

    Attributes
    ----------
            template (Union['AnnotationTemplateCreate', None, Unset]): Template to create. Required if copy_from_queue_id is
                not provided.
            copy_from_queue_id (Union[None, Unset, str]): Source queue ID to copy all templates from. Required if template
                is not provided.
    """

    template: Union["AnnotationTemplateCreate", None, Unset] = UNSET
    copy_from_queue_id: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.annotation_template_create import AnnotationTemplateCreate

        template: None | Unset | dict[str, Any]
        if isinstance(self.template, Unset):
            template = UNSET
        elif isinstance(self.template, AnnotationTemplateCreate):
            template = self.template.to_dict()
        else:
            template = self.template

        copy_from_queue_id: None | Unset | str
        copy_from_queue_id = UNSET if isinstance(self.copy_from_queue_id, Unset) else self.copy_from_queue_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if template is not UNSET:
            field_dict["template"] = template
        if copy_from_queue_id is not UNSET:
            field_dict["copy_from_queue_id"] = copy_from_queue_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_template_create import AnnotationTemplateCreate

        d = dict(src_dict)

        def _parse_template(data: object) -> Union["AnnotationTemplateCreate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationTemplateCreate.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AnnotationTemplateCreate", None, Unset], data)

        template = _parse_template(d.pop("template", UNSET))

        def _parse_copy_from_queue_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        copy_from_queue_id = _parse_copy_from_queue_id(d.pop("copy_from_queue_id", UNSET))

        create_queue_template_request = cls(template=template, copy_from_queue_id=copy_from_queue_id)

        create_queue_template_request.additional_properties = d
        return create_queue_template_request

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
