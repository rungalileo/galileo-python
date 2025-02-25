from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkFeedbackRatingDelete")


@_attrs_define
class BulkFeedbackRatingDelete:
    """
    Attributes:
        feedback_template_id (str):
        operation_type (Union[Literal['delete'], Unset]):  Default: 'delete'.
    """

    feedback_template_id: str
    operation_type: Union[Literal["delete"], Unset] = "delete"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feedback_template_id = self.feedback_template_id

        operation_type = self.operation_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"feedback_template_id": feedback_template_id})
        if operation_type is not UNSET:
            field_dict["operation_type"] = operation_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        feedback_template_id = d.pop("feedback_template_id")

        operation_type = cast(Union[Literal["delete"], Unset], d.pop("operation_type", UNSET))
        if operation_type != "delete" and not isinstance(operation_type, Unset):
            raise ValueError(f"operation_type must match const 'delete', got '{operation_type}'")

        bulk_feedback_rating_delete = cls(feedback_template_id=feedback_template_id, operation_type=operation_type)

        bulk_feedback_rating_delete.additional_properties = d
        return bulk_feedback_rating_delete

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
