from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ruleset import Ruleset


T = TypeVar("T", bound="StageWithRulesets")


@_attrs_define
class StageWithRulesets:
    """
    Attributes:
        name (str): Name of the stage. Must be unique within the project.
        project_id (str): ID of the project to which this stage belongs.
        description (Union[None, Unset, str]): Optional human-readable description of the goals of this guardrail.
        paused (Union[Unset, bool]): Whether the action is enabled. If False, the action will not be applied. Default:
            False.
        prioritized_rulesets (Union[Unset, list['Ruleset']]): Rulesets to be applied to the payload.
        type_ (Union[Unset, Any]): Type of the stage. Default: 'local'.
    """

    name: str
    project_id: str
    description: Union[None, Unset, str] = UNSET
    paused: Union[Unset, bool] = False
    prioritized_rulesets: Union[Unset, list["Ruleset"]] = UNSET
    type_: Union[Unset, Any] = "local"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project_id = self.project_id

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        paused = self.paused

        prioritized_rulesets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.prioritized_rulesets, Unset):
            prioritized_rulesets = []
            for prioritized_rulesets_item_data in self.prioritized_rulesets:
                prioritized_rulesets_item = prioritized_rulesets_item_data.to_dict()
                prioritized_rulesets.append(prioritized_rulesets_item)

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "project_id": project_id})
        if description is not UNSET:
            field_dict["description"] = description
        if paused is not UNSET:
            field_dict["paused"] = paused
        if prioritized_rulesets is not UNSET:
            field_dict["prioritized_rulesets"] = prioritized_rulesets
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.ruleset import Ruleset

        d = src_dict.copy()
        name = d.pop("name")

        project_id = d.pop("project_id")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        paused = d.pop("paused", UNSET)

        prioritized_rulesets = []
        _prioritized_rulesets = d.pop("prioritized_rulesets", UNSET)
        for prioritized_rulesets_item_data in _prioritized_rulesets or []:
            prioritized_rulesets_item = Ruleset.from_dict(prioritized_rulesets_item_data)

            prioritized_rulesets.append(prioritized_rulesets_item)

        type_ = d.pop("type", UNSET)

        stage_with_rulesets = cls(
            name=name,
            project_id=project_id,
            description=description,
            paused=paused,
            prioritized_rulesets=prioritized_rulesets,
            type_=type_,
        )

        stage_with_rulesets.additional_properties = d
        return stage_with_rulesets

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
