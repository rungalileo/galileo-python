from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.output_type_enum import OutputTypeEnum, check_output_type_enum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate


T = TypeVar("T", bound="CreateLLMScorerVersionRequest")


@_attrs_define
class CreateLLMScorerVersionRequest:
    """
    Attributes:
        chain_poll_template (Union['ChainPollTemplate', None, Unset]):
        cot_enabled (Union[None, Unset, bool]):
        instructions (Union[None, Unset, str]):
        model_name (Union[None, Unset, str]):
        num_judges (Union[None, Unset, int]):
        output_type (Union[None, OutputTypeEnum, Unset]):
        scoreable_node_types (Union[None, Unset, list[str]]):
        user_prompt (Union[None, Unset, str]):
    """

    chain_poll_template: Union["ChainPollTemplate", None, Unset] = UNSET
    cot_enabled: Union[None, Unset, bool] = UNSET
    instructions: Union[None, Unset, str] = UNSET
    model_name: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    output_type: Union[None, OutputTypeEnum, Unset] = UNSET
    scoreable_node_types: Union[None, Unset, list[str]] = UNSET
    user_prompt: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_poll_template import ChainPollTemplate

        chain_poll_template: Union[None, Unset, dict[str, Any]]
        if isinstance(self.chain_poll_template, Unset):
            chain_poll_template = UNSET
        elif isinstance(self.chain_poll_template, ChainPollTemplate):
            chain_poll_template = self.chain_poll_template.to_dict()
        else:
            chain_poll_template = self.chain_poll_template

        cot_enabled: Union[None, Unset, bool]
        if isinstance(self.cot_enabled, Unset):
            cot_enabled = UNSET
        else:
            cot_enabled = self.cot_enabled

        instructions: Union[None, Unset, str]
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        model_name: Union[None, Unset, str]
        if isinstance(self.model_name, Unset):
            model_name = UNSET
        else:
            model_name = self.model_name

        num_judges: Union[None, Unset, int]
        if isinstance(self.num_judges, Unset):
            num_judges = UNSET
        else:
            num_judges = self.num_judges

        output_type: Union[None, Unset, str]
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        elif isinstance(self.output_type, str):
            output_type = self.output_type
        else:
            output_type = self.output_type

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        user_prompt: Union[None, Unset, str]
        if isinstance(self.user_prompt, Unset):
            user_prompt = UNSET
        else:
            user_prompt = self.user_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if chain_poll_template is not UNSET:
            field_dict["chain_poll_template"] = chain_poll_template
        if cot_enabled is not UNSET:
            field_dict["cot_enabled"] = cot_enabled
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate

        d = dict(src_dict)

        def _parse_chain_poll_template(data: object) -> Union["ChainPollTemplate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                chain_poll_template_type_0 = ChainPollTemplate.from_dict(data)

                return chain_poll_template_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChainPollTemplate", None, Unset], data)

        chain_poll_template = _parse_chain_poll_template(d.pop("chain_poll_template", UNSET))

        def _parse_cot_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        cot_enabled = _parse_cot_enabled(d.pop("cot_enabled", UNSET))

        def _parse_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        def _parse_model_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        def _parse_num_judges(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        def _parse_output_type(data: object) -> Union[None, OutputTypeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                output_type_type_0 = check_output_type_enum(data)

                return output_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, OutputTypeEnum, Unset], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        def _parse_scoreable_node_types(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scoreable_node_types_type_0 = cast(list[str], data)

                return scoreable_node_types_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        def _parse_user_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

        create_llm_scorer_version_request = cls(
            chain_poll_template=chain_poll_template,
            cot_enabled=cot_enabled,
            instructions=instructions,
            model_name=model_name,
            num_judges=num_judges,
            output_type=output_type,
            scoreable_node_types=scoreable_node_types,
            user_prompt=user_prompt,
        )

        create_llm_scorer_version_request.additional_properties = d
        return create_llm_scorer_version_request

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
