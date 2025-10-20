from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_tags_filter_operator import ScorerTagsFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerTagsFilter")


@_attrs_define
class ScorerTagsFilter:
    """
    Attributes
    ----------
        operator (ScorerTagsFilterOperator):
        value (Union[list[str], str]):
        case_sensitive (Union[Unset, bool]):  Default: True.
        name (Union[Literal['tags'], Unset]):  Default: 'tags'.
    """

    operator: ScorerTagsFilterOperator
    value: Union[list[str], str]
    case_sensitive: Union[Unset, bool] = True
    name: Union[Literal["tags"], Unset] = "tags"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: Union[list[str], str]
        value = self.value if isinstance(self.value, list) else self.value

        case_sensitive = self.case_sensitive

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "value": value})
        if case_sensitive is not UNSET:
            field_dict["case_sensitive"] = case_sensitive
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operator = ScorerTagsFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        value = _parse_value(d.pop("value"))

        case_sensitive = d.pop("case_sensitive", UNSET)

        name = cast(Union[Literal["tags"], Unset], d.pop("name", UNSET))
        if name != "tags" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'tags', got '{name}'")

        scorer_tags_filter = cls(operator=operator, value=value, case_sensitive=case_sensitive, name=name)

        scorer_tags_filter.additional_properties = d
        return scorer_tags_filter

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
