from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseRegisteredScorerDB")


@_attrs_define
class BaseRegisteredScorerDB:
    """
    Attributes
    ----------
        id (str):
        name (str):
        score_type (Union[None, Unset, str]):
    """

    id: str
    name: str
    score_type: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        score_type: Union[None, Unset, str]
        score_type = UNSET if isinstance(self.score_type, Unset) else self.score_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "name": name})
        if score_type is not UNSET:
            field_dict["score_type"] = score_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_score_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        score_type = _parse_score_type(d.pop("score_type", UNSET))

        base_registered_scorer_db = cls(id=id, name=name, score_type=score_type)

        base_registered_scorer_db.additional_properties = d
        return base_registered_scorer_db

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
