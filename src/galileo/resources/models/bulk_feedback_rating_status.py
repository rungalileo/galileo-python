from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.feedback_rating_operation_type import FeedbackRatingOperationType
from ..models.selector_type import SelectorType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkFeedbackRatingStatus")


@_attrs_define
class BulkFeedbackRatingStatus:
    """
    Attributes:
        operation (FeedbackRatingOperationType): Operation type for bulk feedback rating operations.
        success (bool):
        message (None | str):
        selector (SelectorType | Unset):
        index (int | None | Unset):
        trace (None | str | Unset):
    """

    operation: FeedbackRatingOperationType
    success: bool
    message: None | str
    selector: SelectorType | Unset = UNSET
    index: int | None | Unset = UNSET
    trace: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operation = self.operation.value

        success = self.success

        message: None | str
        message = self.message

        selector: str | Unset = UNSET
        if not isinstance(self.selector, Unset):
            selector = self.selector.value

        index: int | None | Unset
        if isinstance(self.index, Unset):
            index = UNSET
        else:
            index = self.index

        trace: None | str | Unset
        if isinstance(self.trace, Unset):
            trace = UNSET
        else:
            trace = self.trace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operation": operation, "success": success, "message": message})
        if selector is not UNSET:
            field_dict["selector"] = selector
        if index is not UNSET:
            field_dict["index"] = index
        if trace is not UNSET:
            field_dict["trace"] = trace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operation = FeedbackRatingOperationType(d.pop("operation"))

        success = d.pop("success")

        def _parse_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        message = _parse_message(d.pop("message"))

        _selector = d.pop("selector", UNSET)
        selector: SelectorType | Unset
        if isinstance(_selector, Unset):
            selector = UNSET
        else:
            selector = SelectorType(_selector)

        def _parse_index(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        index = _parse_index(d.pop("index", UNSET))

        def _parse_trace(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trace = _parse_trace(d.pop("trace", UNSET))

        bulk_feedback_rating_status = cls(
            operation=operation, success=success, message=message, selector=selector, index=index, trace=trace
        )

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
