from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate


T = TypeVar("T", bound="BaseGeneratedScorerDB")


@_attrs_define
class BaseGeneratedScorerDB:
    """
    Attributes:
        chain_poll_template (ChainPollTemplate): Template for a chainpoll metric prompt,
            containing all the info necessary to send a chainpoll prompt.
        id (str):
        name (str):
        instructions (Union[None, Unset, str]):
        user_prompt (Union[None, Unset, str]):
    """

    chain_poll_template: "ChainPollTemplate"
    id: str
    name: str
    instructions: Union[None, Unset, str] = UNSET
    user_prompt: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chain_poll_template = self.chain_poll_template.to_dict()

        id = self.id

        name = self.name

        instructions: Union[None, Unset, str]
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        user_prompt: Union[None, Unset, str]
        if isinstance(self.user_prompt, Unset):
            user_prompt = UNSET
        else:
            user_prompt = self.user_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"chain_poll_template": chain_poll_template, "id": id, "name": name})
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate

        d = dict(src_dict)
        chain_poll_template = ChainPollTemplate.from_dict(d.pop("chain_poll_template"))

        id = d.pop("id")

        name = d.pop("name")

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

        base_generated_scorer_db = cls(
            chain_poll_template=chain_poll_template,
            id=id,
            name=name,
            instructions=instructions,
            user_prompt=user_prompt,
        )

        base_generated_scorer_db.additional_properties = d
        return base_generated_scorer_db

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
