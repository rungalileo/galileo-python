from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subscription_config import SubscriptionConfig


T = TypeVar("T", bound="PassthroughAction")


@_attrs_define
class PassthroughAction:
    """
    Attributes
    ----------
        type_ (Union[Literal['PASSTHROUGH'], Unset]):  Default: 'PASSTHROUGH'.
        subscriptions (Union[Unset, list['SubscriptionConfig']]): List of subscriptions to send a notification to when
            this action is applied and the ruleset status matches any of the configured statuses.
    """

    type_: Union[Literal["PASSTHROUGH"], Unset] = "PASSTHROUGH"
    subscriptions: Union[Unset, list["SubscriptionConfig"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        subscriptions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.subscriptions, Unset):
            subscriptions = []
            for subscriptions_item_data in self.subscriptions:
                subscriptions_item = subscriptions_item_data.to_dict()
                subscriptions.append(subscriptions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if subscriptions is not UNSET:
            field_dict["subscriptions"] = subscriptions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.subscription_config import SubscriptionConfig

        d = dict(src_dict)
        type_ = cast(Union[Literal["PASSTHROUGH"], Unset], d.pop("type", UNSET))
        if type_ != "PASSTHROUGH" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'PASSTHROUGH', got '{type_}'")

        subscriptions = []
        _subscriptions = d.pop("subscriptions", UNSET)
        for subscriptions_item_data in _subscriptions or []:
            subscriptions_item = SubscriptionConfig.from_dict(subscriptions_item_data)

            subscriptions.append(subscriptions_item)

        passthrough_action = cls(type_=type_, subscriptions=subscriptions)

        passthrough_action.additional_properties = d
        return passthrough_action

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
