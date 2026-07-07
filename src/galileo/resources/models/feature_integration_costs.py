from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_integration_costs import ProjectIntegrationCosts


T = TypeVar("T", bound="FeatureIntegrationCosts")


@_attrs_define
class FeatureIntegrationCosts:
    """
    Attributes:
        feature_name (str):
        total_cost (Union[Unset, float]):  Default: 0.0.
        projects (Union[Unset, list['ProjectIntegrationCosts']]):
    """

    feature_name: str
    total_cost: Union[Unset, float] = 0.0
    projects: Union[Unset, list["ProjectIntegrationCosts"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feature_name = self.feature_name

        total_cost = self.total_cost

        projects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = []
            for projects_item_data in self.projects:
                projects_item = projects_item_data.to_dict()
                projects.append(projects_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"feature_name": feature_name})
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost
        if projects is not UNSET:
            field_dict["projects"] = projects

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_integration_costs import ProjectIntegrationCosts

        d = dict(src_dict)
        feature_name = d.pop("feature_name")

        total_cost = d.pop("total_cost", UNSET)

        projects = []
        _projects = d.pop("projects", UNSET)
        for projects_item_data in _projects or []:
            projects_item = ProjectIntegrationCosts.from_dict(projects_item_data)

            projects.append(projects_item)

        feature_integration_costs = cls(feature_name=feature_name, total_cost=total_cost, projects=projects)

        feature_integration_costs.additional_properties = d
        return feature_integration_costs

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
