from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.generated_scorer_configuration import GeneratedScorerConfiguration


T = TypeVar("T", bound="CreateGeneratedScorerRequest")


@_attrs_define
class CreateGeneratedScorerRequest:
    """
    Attributes:
        name (str):
        chain_poll_template (ChainPollTemplate): Template for a chainpoll metric prompt,
            containing all the info necessary to send a chainpoll prompt.
        instructions (None | str | Unset):
        scoreable_node_types (list[NodeType] | None | Unset):
        scorer_configuration (GeneratedScorerConfiguration | Unset):
        user_prompt (None | str | Unset):
    """

    name: str
    chain_poll_template: ChainPollTemplate
    instructions: None | str | Unset = UNSET
    scoreable_node_types: list[NodeType] | None | Unset = UNSET
    scorer_configuration: GeneratedScorerConfiguration | Unset = UNSET
    user_prompt: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        chain_poll_template = self.chain_poll_template.to_dict()

        instructions: None | str | Unset
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        scoreable_node_types: list[str] | None | Unset
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = []
            for scoreable_node_types_type_0_item_data in self.scoreable_node_types:
                scoreable_node_types_type_0_item = scoreable_node_types_type_0_item_data.value
                scoreable_node_types.append(scoreable_node_types_type_0_item)

        else:
            scoreable_node_types = self.scoreable_node_types

        scorer_configuration: dict[str, Any] | Unset = UNSET
        if not isinstance(self.scorer_configuration, Unset):
            scorer_configuration = self.scorer_configuration.to_dict()

        user_prompt: None | str | Unset
        if isinstance(self.user_prompt, Unset):
            user_prompt = UNSET
        else:
            user_prompt = self.user_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "chain_poll_template": chain_poll_template})
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if scorer_configuration is not UNSET:
            field_dict["scorer_configuration"] = scorer_configuration
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.generated_scorer_configuration import GeneratedScorerConfiguration

        d = dict(src_dict)
        name = d.pop("name")

        chain_poll_template = ChainPollTemplate.from_dict(d.pop("chain_poll_template"))

        def _parse_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        def _parse_scoreable_node_types(data: object) -> list[NodeType] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scoreable_node_types_type_0 = []
                _scoreable_node_types_type_0 = data
                for scoreable_node_types_type_0_item_data in _scoreable_node_types_type_0:
                    scoreable_node_types_type_0_item = NodeType(scoreable_node_types_type_0_item_data)

                    scoreable_node_types_type_0.append(scoreable_node_types_type_0_item)

                return scoreable_node_types_type_0
            except:  # noqa: E722
                pass
            return cast(list[NodeType] | None | Unset, data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        _scorer_configuration = d.pop("scorer_configuration", UNSET)
        scorer_configuration: GeneratedScorerConfiguration | Unset
        if isinstance(_scorer_configuration, Unset):
            scorer_configuration = UNSET
        else:
            scorer_configuration = GeneratedScorerConfiguration.from_dict(_scorer_configuration)

        def _parse_user_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

        create_generated_scorer_request = cls(
            name=name,
            chain_poll_template=chain_poll_template,
            instructions=instructions,
            scoreable_node_types=scoreable_node_types,
            scorer_configuration=scorer_configuration,
            user_prompt=user_prompt,
        )

        create_generated_scorer_request.additional_properties = d
        return create_generated_scorer_request

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
