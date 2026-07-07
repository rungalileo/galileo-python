from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerScopeProjectsFilter")


@_attrs_define
class ScorerScopeProjectsFilter:
    """Matches scorers whose access scope (scorer_projects) includes ANY of the
    given project ids. include_global=True additionally matches global scorers
    ("metrics available in project X").

    Distinct from the run-usage "projects used" relation (scorers_to_projects /
    GET /scorers/{scorer_id}/projects), which tracks where a scorer has run.

        Attributes:
            project_ids (list[str]):
            name (Union[Literal['scope_projects'], Unset]):  Default: 'scope_projects'.
            include_global (Union[Unset, bool]):  Default: False.
    """

    project_ids: list[str]
    name: Union[Literal["scope_projects"], Unset] = "scope_projects"
    include_global: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_ids = self.project_ids

        name = self.name

        include_global = self.include_global

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_ids": project_ids})
        if name is not UNSET:
            field_dict["name"] = name
        if include_global is not UNSET:
            field_dict["include_global"] = include_global

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_ids = cast(list[str], d.pop("project_ids"))

        name = cast(Union[Literal["scope_projects"], Unset], d.pop("name", UNSET))
        if name != "scope_projects" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'scope_projects', got '{name}'")

        include_global = d.pop("include_global", UNSET)

        scorer_scope_projects_filter = cls(project_ids=project_ids, name=name, include_global=include_global)

        scorer_scope_projects_filter.additional_properties = d
        return scorer_scope_projects_filter

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
