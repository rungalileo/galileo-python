from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FeedbackTemplateUpdate")


@_attrs_define
class FeedbackTemplateUpdate:
    """
    Attributes:
        criteria (Union[None, str]):
        name (str):
    """

    criteria: Union[None, str]
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        criteria: Union[None, str]
        criteria = self.criteria

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"criteria": criteria, "name": name})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_criteria(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        criteria = _parse_criteria(d.pop("criteria"))

        name = d.pop("name")

        feedback_template_update = cls(criteria=criteria, name=name)

        feedback_template_update.additional_properties = d
        return feedback_template_update

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
