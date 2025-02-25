import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.weekly_changelog_changes import WeeklyChangelogChanges


T = TypeVar("T", bound="WeeklyChangelog")


@_attrs_define
class WeeklyChangelog:
    """
    Attributes:
        week_of (datetime.date):
        changes (Union[Unset, WeeklyChangelogChanges]):
    """

    week_of: datetime.date
    changes: Union[Unset, "WeeklyChangelogChanges"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        week_of = self.week_of.isoformat()

        changes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.changes, Unset):
            changes = self.changes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"week_of": week_of})
        if changes is not UNSET:
            field_dict["changes"] = changes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.weekly_changelog_changes import WeeklyChangelogChanges

        d = src_dict.copy()
        week_of = isoparse(d.pop("week_of")).date()

        _changes = d.pop("changes", UNSET)
        changes: Union[Unset, WeeklyChangelogChanges]
        if isinstance(_changes, Unset):
            changes = UNSET
        else:
            changes = WeeklyChangelogChanges.from_dict(_changes)

        weekly_changelog = cls(week_of=week_of, changes=changes)

        weekly_changelog.additional_properties = d
        return weekly_changelog

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
