from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_label_filter_operator import ScorerLabelFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerLabelFilter")


@_attrs_define
class ScorerLabelFilter:
    """
    Attributes
    ----------
        operator (ScorerLabelFilterOperator):
        value (Union[list[str], str]):
        name (Union[Literal['label'], Unset]):  Default: 'label'.
        case_sensitive (Union[Unset, bool]):  Default: True.
    """

    operator: ScorerLabelFilterOperator
    value: Union[list[str], str]
    name: Union[Literal["label"], Unset] = "label"
    case_sensitive: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: Union[list[str], str]
        value = self.value if isinstance(self.value, list) else self.value

        name = self.name

        case_sensitive = self.case_sensitive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "value": value})
        if name is not UNSET:
            field_dict["name"] = name
        if case_sensitive is not UNSET:
            field_dict["case_sensitive"] = case_sensitive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operator = ScorerLabelFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["label"], Unset], d.pop("name", UNSET))
        if name != "label" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'label', got '{name}'")

        case_sensitive = d.pop("case_sensitive", UNSET)

        scorer_label_filter = cls(operator=operator, value=value, name=name, case_sensitive=case_sensitive)

        scorer_label_filter.additional_properties = d
        return scorer_label_filter

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
