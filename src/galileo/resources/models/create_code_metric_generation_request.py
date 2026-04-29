from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCodeMetricGenerationRequest")


@_attrs_define
class CreateCodeMetricGenerationRequest:
    """Request to generate scorer code from a user message.

    Attributes
    ----------
        user_message (str): Natural language, code, or combination
        node_type (Union[None, Unset, str]): Selected scoreable node type (llm, retriever, trace, agent, workflow, tool,
            session)
        model_name (Union[None, Unset, str]): Model alias to use for generation. Defaults to best available.
    """

    user_message: str
    node_type: None | Unset | str = UNSET
    model_name: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_message = self.user_message

        node_type: None | Unset | str
        node_type = UNSET if isinstance(self.node_type, Unset) else self.node_type

        model_name: None | Unset | str
        model_name = UNSET if isinstance(self.model_name, Unset) else self.model_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"user_message": user_message})
        if node_type is not UNSET:
            field_dict["node_type"] = node_type
        if model_name is not UNSET:
            field_dict["model_name"] = model_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_message = d.pop("user_message")

        def _parse_node_type(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        node_type = _parse_node_type(d.pop("node_type", UNSET))

        def _parse_model_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        create_code_metric_generation_request = cls(
            user_message=user_message, node_type=node_type, model_name=model_name
        )

        create_code_metric_generation_request.additional_properties = d
        return create_code_metric_generation_request

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
