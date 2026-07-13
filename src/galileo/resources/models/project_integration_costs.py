from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_costs_data_point import IntegrationCostsDataPoint


T = TypeVar("T", bound="ProjectIntegrationCosts")


@_attrs_define
class ProjectIntegrationCosts:
    """
    Attributes
    ----------
        project_id (str):
        project_name (str):
        total_cost (Union[Unset, float]):  Default: 0.0.
        data_points (Union[Unset, list['IntegrationCostsDataPoint']]):
    """

    project_id: str
    project_name: str
    total_cost: Unset | float = 0.0
    data_points: Unset | list["IntegrationCostsDataPoint"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        project_name = self.project_name

        total_cost = self.total_cost

        data_points: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.data_points, Unset):
            data_points = []
            for data_points_item_data in self.data_points:
                data_points_item = data_points_item_data.to_dict()
                data_points.append(data_points_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "project_name": project_name})
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost
        if data_points is not UNSET:
            field_dict["data_points"] = data_points

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_costs_data_point import IntegrationCostsDataPoint

        d = dict(src_dict)
        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        total_cost = d.pop("total_cost", UNSET)

        data_points = []
        _data_points = d.pop("data_points", UNSET)
        for data_points_item_data in _data_points or []:
            data_points_item = IntegrationCostsDataPoint.from_dict(data_points_item_data)

            data_points.append(data_points_item)

        project_integration_costs = cls(
            project_id=project_id, project_name=project_name, total_cost=total_cost, data_points=data_points
        )

        project_integration_costs.additional_properties = d
        return project_integration_costs

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
