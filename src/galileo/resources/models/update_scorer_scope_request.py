from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateScorerScopeRequest")


@_attrs_define
class UpdateScorerScopeRequest:
    """Full-replace access scope update for a scorer (Share / manage visibility).

    is_global=True promotes the scorer to global (org admin only; project_ids
    must be empty). is_global=False scopes the scorer to exactly project_ids.

        Attributes:
            is_global (bool):
            project_ids (Union[Unset, list[str]]):
    """

    is_global: bool
    project_ids: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_global = self.is_global

        project_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.project_ids, Unset):
            project_ids = self.project_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"is_global": is_global})
        if project_ids is not UNSET:
            field_dict["project_ids"] = project_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_global = d.pop("is_global")

        project_ids = cast(list[str], d.pop("project_ids", UNSET))

        update_scorer_scope_request = cls(is_global=is_global, project_ids=project_ids)

        update_scorer_scope_request.additional_properties = d
        return update_scorer_scope_request

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
