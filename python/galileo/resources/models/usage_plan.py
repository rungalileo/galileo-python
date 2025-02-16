from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UsagePlan")


@_attrs_define
class UsagePlan:
    """
    Attributes:
        max_data_visibility_days (int):
        max_organizations_per_user (int):
        max_payload_size_bytes (int):
        max_traces_per_month (int):
        max_users_per_organization (int):
    """

    max_data_visibility_days: int
    max_organizations_per_user: int
    max_payload_size_bytes: int
    max_traces_per_month: int
    max_users_per_organization: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_data_visibility_days = self.max_data_visibility_days

        max_organizations_per_user = self.max_organizations_per_user

        max_payload_size_bytes = self.max_payload_size_bytes

        max_traces_per_month = self.max_traces_per_month

        max_users_per_organization = self.max_users_per_organization

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_data_visibility_days": max_data_visibility_days,
                "max_organizations_per_user": max_organizations_per_user,
                "max_payload_size_bytes": max_payload_size_bytes,
                "max_traces_per_month": max_traces_per_month,
                "max_users_per_organization": max_users_per_organization,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        max_data_visibility_days = d.pop("max_data_visibility_days")

        max_organizations_per_user = d.pop("max_organizations_per_user")

        max_payload_size_bytes = d.pop("max_payload_size_bytes")

        max_traces_per_month = d.pop("max_traces_per_month")

        max_users_per_organization = d.pop("max_users_per_organization")

        usage_plan = cls(
            max_data_visibility_days=max_data_visibility_days,
            max_organizations_per_user=max_organizations_per_user,
            max_payload_size_bytes=max_payload_size_bytes,
            max_traces_per_month=max_traces_per_month,
            max_users_per_organization=max_users_per_organization,
        )

        usage_plan.additional_properties = d
        return usage_plan

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
