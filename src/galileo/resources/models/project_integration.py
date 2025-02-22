from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectIntegration")


@_attrs_define
class ProjectIntegration:
    """
    Attributes:
        models (list[str]):
        scorer_models (list[str]):
    """

    models: list[str]
    scorer_models: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        models = self.models

        scorer_models = self.scorer_models

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"models": models, "scorer_models": scorer_models})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        models = cast(list[str], d.pop("models"))

        scorer_models = cast(list[str], d.pop("scorer_models"))

        project_integration = cls(models=models, scorer_models=scorer_models)

        project_integration.additional_properties = d
        return project_integration

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
