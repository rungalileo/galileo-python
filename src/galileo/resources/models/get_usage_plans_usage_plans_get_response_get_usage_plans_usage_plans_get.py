from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.usage_plan import UsagePlan


T = TypeVar("T", bound="GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet")


@_attrs_define
class GetUsagePlansUsagePlansGetResponseGetUsagePlansUsagePlansGet:
    """ """

    additional_properties: dict[str, "UsagePlan"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.usage_plan import UsagePlan

        d = src_dict.copy()
        get_usage_plans_usage_plans_get_response_get_usage_plans_usage_plans_get = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = UsagePlan.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_usage_plans_usage_plans_get_response_get_usage_plans_usage_plans_get.additional_properties = (
            additional_properties
        )
        return get_usage_plans_usage_plans_get_response_get_usage_plans_usage_plans_get

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "UsagePlan":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "UsagePlan") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
