from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricInputs")


@_attrs_define
class MetricInputs:
    """Metric inputs for a prompt template.
    Include an optional inputs_config to help formatting with a prompt template.

        Attributes:
            query (str):
            response (str):
            ground_truth (Union[None, Unset, str]):
            tools (Union[None, Unset, str]):
    """

    query: str
    response: str
    ground_truth: Union[None, Unset, str] = UNSET
    tools: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        response = self.response

        ground_truth: Union[None, Unset, str]
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        tools: Union[None, Unset, str]
        if isinstance(self.tools, Unset):
            tools = UNSET
        else:
            tools = self.tools

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"query": query, "response": response})
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query")

        response = d.pop("response")

        def _parse_ground_truth(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        metric_inputs = cls(query=query, response=response, ground_truth=ground_truth, tools=tools)

        metric_inputs.additional_properties = d
        return metric_inputs

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
