import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.generated_scorer_configuration import GeneratedScorerConfiguration


T = TypeVar("T", bound="GeneratedScorerResponse")


@_attrs_define
class GeneratedScorerResponse:
    """
    Attributes
    ----------
        id (str):
        name (str):
        chain_poll_template (ChainPollTemplate): Template for a chainpoll metric prompt,
            containing all the info necessary to send a chainpoll prompt.
        created_by (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        scoreable_node_types (Union[None, list[NodeType]]):
        scorer_configuration (GeneratedScorerConfiguration):
        instructions (Union[None, Unset, str]):
        user_prompt (Union[None, Unset, str]):
    """

    id: str
    name: str
    chain_poll_template: "ChainPollTemplate"
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    scoreable_node_types: Union[None, list[NodeType]]
    scorer_configuration: "GeneratedScorerConfiguration"
    instructions: Union[None, Unset, str] = UNSET
    user_prompt: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        chain_poll_template = self.chain_poll_template.to_dict()

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        scoreable_node_types: Union[None, list[str]]
        if isinstance(self.scoreable_node_types, list):
            scoreable_node_types = []
            for scoreable_node_types_type_0_item_data in self.scoreable_node_types:
                scoreable_node_types_type_0_item = scoreable_node_types_type_0_item_data.value
                scoreable_node_types.append(scoreable_node_types_type_0_item)

        else:
            scoreable_node_types = self.scoreable_node_types

        scorer_configuration = self.scorer_configuration.to_dict()

        instructions: Union[None, Unset, str]
        instructions = UNSET if isinstance(self.instructions, Unset) else self.instructions

        user_prompt: Union[None, Unset, str]
        user_prompt = UNSET if isinstance(self.user_prompt, Unset) else self.user_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "chain_poll_template": chain_poll_template,
                "created_by": created_by,
                "created_at": created_at,
                "updated_at": updated_at,
                "scoreable_node_types": scoreable_node_types,
                "scorer_configuration": scorer_configuration,
            }
        )
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.generated_scorer_configuration import GeneratedScorerConfiguration

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        chain_poll_template = ChainPollTemplate.from_dict(d.pop("chain_poll_template"))

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_scoreable_node_types(data: object) -> Union[None, list[NodeType]]:
            if data is None:
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
            return cast(Union[None, list[NodeType]], data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types"))

        scorer_configuration = GeneratedScorerConfiguration.from_dict(d.pop("scorer_configuration"))

        def _parse_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        def _parse_user_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

        generated_scorer_response = cls(
            id=id,
            name=name,
            chain_poll_template=chain_poll_template,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
            scoreable_node_types=scoreable_node_types,
            scorer_configuration=scorer_configuration,
            instructions=instructions,
            user_prompt=user_prompt,
        )

        generated_scorer_response.additional_properties = d
        return generated_scorer_response

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
