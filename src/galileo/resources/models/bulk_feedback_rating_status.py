from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.feedback_rating_operation_type import FeedbackRatingOperationType

T = TypeVar("T", bound="BulkFeedbackRatingStatus")


@_attrs_define
class BulkFeedbackRatingStatus:
    """
    Attributes:
        index (int):
        message (Union[None, str]):
        operation (FeedbackRatingOperationType): Operation type for bulk feedback rating operations.
        success (bool):
    """

    index: int
    message: Union[None, str]
    operation: FeedbackRatingOperationType
    success: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        message: Union[None, str]
        message = self.message

        operation = self.operation.value

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"index": index, "message": message, "operation": operation, "success": success})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        index = d.pop("index")

        def _parse_message(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        message = _parse_message(d.pop("message"))

        operation = FeedbackRatingOperationType(d.pop("operation"))

        success = d.pop("success")

        bulk_feedback_rating_status = cls(index=index, message=message, operation=operation, success=success)

        bulk_feedback_rating_status.additional_properties = d
        return bulk_feedback_rating_status

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
