from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.stage_type import StageType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ruleset import Ruleset


T = TypeVar("T", bound="StageWithRulesets")


@_attrs_define
class StageWithRulesets:
    """
    Attributes
    ----------
        name (str): Name of the stage. Must be unique within the project.
        project_id (str): ID of the project to which this stage belongs.
        prioritized_rulesets (Union[Unset, list['Ruleset']]): Rulesets to be applied to the payload.
        description (Union[None, Unset, str]): Optional human-readable description of the goals of this guardrail.
        type_ (Union[Unset, StageType]):
        paused (Union[Unset, bool]): Whether the action is enabled. If False, the action will not be applied. Default:
            False.
    """

    name: str
    project_id: str
    prioritized_rulesets: Union[Unset, list["Ruleset"]] = UNSET
    description: Union[None, Unset, str] = UNSET
    type_: Union[Unset, StageType] = UNSET
    paused: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project_id = self.project_id

        prioritized_rulesets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.prioritized_rulesets, Unset):
            prioritized_rulesets = []
            for prioritized_rulesets_item_data in self.prioritized_rulesets:
                prioritized_rulesets_item = prioritized_rulesets_item_data.to_dict()
                prioritized_rulesets.append(prioritized_rulesets_item)

        description: Union[None, Unset, str]
        description = UNSET if isinstance(self.description, Unset) else self.description

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        paused = self.paused

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "project_id": project_id})
        if prioritized_rulesets is not UNSET:
            field_dict["prioritized_rulesets"] = prioritized_rulesets
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if paused is not UNSET:
            field_dict["paused"] = paused

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ruleset import Ruleset

        d = dict(src_dict)
        name = d.pop("name")

        project_id = d.pop("project_id")

        prioritized_rulesets = []
        _prioritized_rulesets = d.pop("prioritized_rulesets", UNSET)
        for prioritized_rulesets_item_data in _prioritized_rulesets or []:
            prioritized_rulesets_item = Ruleset.from_dict(prioritized_rulesets_item_data)

            prioritized_rulesets.append(prioritized_rulesets_item)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, StageType]
        type_ = UNSET if isinstance(_type_, Unset) else StageType(_type_)

        paused = d.pop("paused", UNSET)

        stage_with_rulesets = cls(
            name=name,
            project_id=project_id,
            prioritized_rulesets=prioritized_rulesets,
            description=description,
            type_=type_,
            paused=paused,
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
