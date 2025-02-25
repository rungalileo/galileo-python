from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FeatureColumnsResponse")


@_attrs_define
class FeatureColumnsResponse:
    """
    Attributes:
        feature_names (list[str]):
        project_id (str):
        run_id (str):
    """

    feature_names: list[str]
    project_id: str
    run_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feature_names = self.feature_names

        project_id = self.project_id

        run_id = self.run_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"feature_names": feature_names, "project_id": project_id, "run_id": run_id})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        feature_names = cast(list[str], d.pop("feature_names"))

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        feature_columns_response = cls(feature_names=feature_names, project_id=project_id, run_id=run_id)

        feature_columns_response.additional_properties = d
        return feature_columns_response

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
