from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.generated_scorer_configuration import GeneratedScorerConfiguration


T = TypeVar("T", bound="UpdateGeneratedScorerRequest")


@_attrs_define
class UpdateGeneratedScorerRequest:
    """
    Attributes:
        chain_poll_template (Union['ChainPollTemplate', None, Unset]):
        instructions (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        scoreable_node_types (Union[None, Unset, list[NodeType]]):
        scorer_configuration (Union['GeneratedScorerConfiguration', None, Unset]):
    """

    chain_poll_template: Union["ChainPollTemplate", None, Unset] = UNSET
    instructions: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    scoreable_node_types: Union[None, Unset, list[NodeType]] = UNSET
    scorer_configuration: Union["GeneratedScorerConfiguration", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.generated_scorer_configuration import GeneratedScorerConfiguration

        chain_poll_template: Union[None, Unset, dict[str, Any]]
        if isinstance(self.chain_poll_template, Unset):
            chain_poll_template = UNSET
        elif isinstance(self.chain_poll_template, ChainPollTemplate):
            chain_poll_template = self.chain_poll_template.to_dict()
        else:
            chain_poll_template = self.chain_poll_template

        instructions: Union[None, Unset, str]
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = []
            for scoreable_node_types_type_0_item_data in self.scoreable_node_types:
                scoreable_node_types_type_0_item = scoreable_node_types_type_0_item_data.value
                scoreable_node_types.append(scoreable_node_types_type_0_item)

        else:
            scoreable_node_types = self.scoreable_node_types

        scorer_configuration: Union[None, Unset, dict[str, Any]]
        if isinstance(self.scorer_configuration, Unset):
            scorer_configuration = UNSET
        elif isinstance(self.scorer_configuration, GeneratedScorerConfiguration):
            scorer_configuration = self.scorer_configuration.to_dict()
        else:
            scorer_configuration = self.scorer_configuration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if chain_poll_template is not UNSET:
            field_dict["chain_poll_template"] = chain_poll_template
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if name is not UNSET:
            field_dict["name"] = name
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if scorer_configuration is not UNSET:
            field_dict["scorer_configuration"] = scorer_configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.generated_scorer_configuration import GeneratedScorerConfiguration

        d = src_dict.copy()

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

        def _parse_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_scoreable_node_types(data: object) -> Union[None, Unset, list[NodeType]]:
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
            return cast(Union[None, Unset, list[NodeType]], data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        def _parse_scorer_configuration(data: object) -> Union["GeneratedScorerConfiguration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scorer_configuration_type_0 = GeneratedScorerConfiguration.from_dict(data)

                return scorer_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GeneratedScorerConfiguration", None, Unset], data)

        scorer_configuration = _parse_scorer_configuration(d.pop("scorer_configuration", UNSET))

        update_generated_scorer_request = cls(
            chain_poll_template=chain_poll_template,
            instructions=instructions,
            name=name,
            scoreable_node_types=scoreable_node_types,
            scorer_configuration=scorer_configuration,
        )

        update_generated_scorer_request.additional_properties = d
        return update_generated_scorer_request

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
