from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.generic_action import GenericAction
from ..models.resource_kind import ResourceKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="GenericPermission")


@_attrs_define
class GenericPermission:
    """Generic permissions describe what a user GENERALLY can and cannot do.

    The actions are not specific to a resource instance (e.g. create). More fine-grained permissions should also be set
    in the authorization policies.

        Attributes:
            resource (ResourceKind):
            action (GenericAction):
            allowed (bool):
            message (None | str | Unset):
    """

    resource: ResourceKind
    action: GenericAction
    allowed: bool
    message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource = self.resource.value

        action = self.action.value

        allowed = self.allowed

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"resource": resource, "action": action, "allowed": allowed})
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource = ResourceKind(d.pop("resource"))

        action = GenericAction(d.pop("action"))

        allowed = d.pop("allowed")

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        generic_permission = cls(resource=resource, action=action, allowed=allowed, message=message)

        generic_permission.additional_properties = d
        return generic_permission

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
