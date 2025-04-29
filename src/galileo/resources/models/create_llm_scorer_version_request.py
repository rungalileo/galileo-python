from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate


T = TypeVar("T", bound="CreateLLMScorerVersionRequest")


@_attrs_define
class CreateLLMScorerVersionRequest:
    """
    Attributes:
        chain_poll_template (ChainPollTemplate): Template for a chainpoll metric prompt,
            containing all the info necessary to send a chainpoll prompt.
        instructions (str):
    """

    chain_poll_template: "ChainPollTemplate"
    instructions: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chain_poll_template = self.chain_poll_template.to_dict()

        instructions = self.instructions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"chain_poll_template": chain_poll_template, "instructions": instructions})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate

        d = src_dict.copy()
        chain_poll_template = ChainPollTemplate.from_dict(d.pop("chain_poll_template"))

        instructions = d.pop("instructions")

        create_llm_scorer_version_request = cls(chain_poll_template=chain_poll_template, instructions=instructions)

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
