from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

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
        version_description (Union[None, Unset, str]):
    """

    chain_poll_template: "ChainPollTemplate"
    instructions: str
    version_description: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chain_poll_template = self.chain_poll_template.to_dict()

        instructions = self.instructions

        version_description: Union[None, Unset, str]
        if isinstance(self.version_description, Unset):
            version_description = UNSET
        else:
            version_description = self.version_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"chain_poll_template": chain_poll_template, "instructions": instructions})
        if version_description is not UNSET:
            field_dict["version_description"] = version_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate

        d = src_dict.copy()
        chain_poll_template = ChainPollTemplate.from_dict(d.pop("chain_poll_template"))

        instructions = d.pop("instructions")

        def _parse_version_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        version_description = _parse_version_description(d.pop("version_description", UNSET))

        create_llm_scorer_version_request = cls(
            chain_poll_template=chain_poll_template, instructions=instructions, version_description=version_description
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
