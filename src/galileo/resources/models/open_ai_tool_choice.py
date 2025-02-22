from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_ai_function import OpenAIFunction


T = TypeVar("T", bound="OpenAIToolChoice")


@_attrs_define
class OpenAIToolChoice:
    """
    Attributes:
        function (OpenAIFunction):
        type_ (Union[Unset, str]):  Default: 'function'.
    """

    function: "OpenAIFunction"
    type_: Union[Unset, str] = "function"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        function = self.function.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"function": function})
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.open_ai_function import OpenAIFunction

        d = src_dict.copy()
        function = OpenAIFunction.from_dict(d.pop("function"))

        type_ = d.pop("type", UNSET)

        open_ai_tool_choice = cls(function=function, type_=type_)

        open_ai_tool_choice.additional_properties = d
        return open_ai_tool_choice

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
