from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TopKToken")


@_attrs_define
class TopKToken:
    """Representation of a token and its probability for Segment Top k logprob tokens.

    Attributes:
        token: The text of the token
        prob: The probability of the token

        Attributes:
            prob (float):
            token (str):
    """

    prob: float
    token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prob = self.prob

        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"prob": prob, "token": token})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prob = d.pop("prob")

        token = d.pop("token")

        top_k_token = cls(prob=prob, token=token)

        top_k_token.additional_properties = d
        return top_k_token

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
