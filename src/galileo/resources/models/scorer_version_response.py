from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate


T = TypeVar("T", bound="ScorerVersionResponse")


@_attrs_define
class ScorerVersionResponse:
    """
    Attributes:
        scorer_content (Union['ChainPollTemplate', str]): chainpoll template for llm based scorers and the code as a
            string for code based scorers
    """

    scorer_content: Union["ChainPollTemplate", str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_poll_template import ChainPollTemplate

        scorer_content: Union[dict[str, Any], str]
        if isinstance(self.scorer_content, ChainPollTemplate):
            scorer_content = self.scorer_content.to_dict()
        else:
            scorer_content = self.scorer_content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"scorer_content": scorer_content})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate

        d = src_dict.copy()

        def _parse_scorer_content(data: object) -> Union["ChainPollTemplate", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scorer_content_type_0 = ChainPollTemplate.from_dict(data)

                return scorer_content_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChainPollTemplate", str], data)

        scorer_content = _parse_scorer_content(d.pop("scorer_content"))

        scorer_version_response = cls(scorer_content=scorer_content)

        scorer_version_response.additional_properties = d
        return scorer_version_response

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
