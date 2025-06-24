from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.feedback_rating_info_feedback_type import FeedbackRatingInfoFeedbackType

T = TypeVar("T", bound="FeedbackRatingInfo")


@_attrs_define
class FeedbackRatingInfo:
    """
    Attributes:
        explanation (str):
        feedback_type (FeedbackRatingInfoFeedbackType):
        value (Union[bool, int, list[str], str]):
    """

    explanation: str
    feedback_type: FeedbackRatingInfoFeedbackType
    value: Union[bool, int, list[str], str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        explanation = self.explanation

        feedback_type = self.feedback_type.value

        value: Union[bool, int, list[str], str]
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"explanation": explanation, "feedback_type": feedback_type, "value": value})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        explanation = d.pop("explanation")

        feedback_type = FeedbackRatingInfoFeedbackType(d.pop("feedback_type"))

        def _parse_value(data: object) -> Union[bool, int, list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_2 = cast(list[str], data)

                return value_type_2
            except:  # noqa: E722
                pass
            return cast(Union[bool, int, list[str], str], data)

        value = _parse_value(d.pop("value"))

        feedback_rating_info = cls(explanation=explanation, feedback_type=feedback_type, value=value)

        feedback_rating_info.additional_properties = d
        return feedback_rating_info

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
