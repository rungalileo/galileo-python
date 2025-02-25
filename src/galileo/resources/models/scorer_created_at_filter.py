import datetime
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.scorer_created_at_filter_operator import ScorerCreatedAtFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerCreatedAtFilter")


@_attrs_define
class ScorerCreatedAtFilter:
    """
    Attributes:
        operator (ScorerCreatedAtFilterOperator):
        value (datetime.datetime):
        name (Union[Literal['created_at'], Unset]):  Default: 'created_at'.
    """

    operator: ScorerCreatedAtFilterOperator
    value: datetime.datetime
    name: Union[Literal["created_at"], Unset] = "created_at"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value = self.value.isoformat()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "value": value})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        operator = ScorerCreatedAtFilterOperator(d.pop("operator"))

        value = isoparse(d.pop("value"))

        name = cast(Union[Literal["created_at"], Unset], d.pop("name", UNSET))
        if name != "created_at" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'created_at', got '{name}'")

        scorer_created_at_filter = cls(operator=operator, value=value, name=name)

        scorer_created_at_filter.additional_properties = d
        return scorer_created_at_filter

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
