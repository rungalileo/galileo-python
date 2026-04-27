from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.generated_scorer_configuration import GeneratedScorerConfiguration


T = TypeVar("T", bound="GeneratedScorerValidationRequest")


@_attrs_define
class GeneratedScorerValidationRequest:
    """Info necessary to execute a generated scorer validation job.

    Attributes:
        query (str):
        response (str):
        chain_poll_template (ChainPollTemplate): Template for a chainpoll metric prompt,
            containing all the info necessary to send a chainpoll prompt.
        scorer_configuration (GeneratedScorerConfiguration):
    """

    query: str
    response: str
    chain_poll_template: ChainPollTemplate
    scorer_configuration: GeneratedScorerConfiguration
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        response = self.response

        chain_poll_template = self.chain_poll_template.to_dict()

        scorer_configuration = self.scorer_configuration.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "response": response,
                "chain_poll_template": chain_poll_template,
                "scorer_configuration": scorer_configuration,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.generated_scorer_configuration import GeneratedScorerConfiguration

        d = dict(src_dict)
        query = d.pop("query")

        response = d.pop("response")

        chain_poll_template = ChainPollTemplate.from_dict(d.pop("chain_poll_template"))

        scorer_configuration = GeneratedScorerConfiguration.from_dict(d.pop("scorer_configuration"))

        generated_scorer_validation_request = cls(
            query=query,
            response=response,
            chain_poll_template=chain_poll_template,
            scorer_configuration=scorer_configuration,
        )

        generated_scorer_validation_request.additional_properties = d
        return generated_scorer_validation_request

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
