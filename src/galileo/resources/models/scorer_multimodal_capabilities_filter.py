from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_multimodal_capabilities_filter_operator import ScorerMultimodalCapabilitiesFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerMultimodalCapabilitiesFilter")


@_attrs_define
class ScorerMultimodalCapabilitiesFilter:
    """Filter scorers by multimodal_capabilities.

    Use operator ``contains`` to match scorers that support a single capability
    (e.g. ``{"name": "multimodal_capabilities", "operator": "contains", "value": "vision"}``).
    Use ``one_of`` to match scorers whose capabilities include ANY of the given
    values (e.g. ``{"name": "multimodal_capabilities", "operator": "one_of", "value": ["vision", "audio"]}``).

        Attributes:
            operator (ScorerMultimodalCapabilitiesFilterOperator):
            value (Union[list[str], str]):
            name (Union[Literal['multimodal_capabilities'], Unset]):  Default: 'multimodal_capabilities'.
            case_sensitive (Union[Unset, bool]):  Default: True.
    """

    operator: ScorerMultimodalCapabilitiesFilterOperator
    value: Union[list[str], str]
    name: Union[Literal["multimodal_capabilities"], Unset] = "multimodal_capabilities"
    case_sensitive: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: Union[list[str], str]
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

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
        operator = ScorerMultimodalCapabilitiesFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[str], data)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["multimodal_capabilities"], Unset], d.pop("name", UNSET))
        if name != "multimodal_capabilities" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'multimodal_capabilities', got '{name}'")

        case_sensitive = d.pop("case_sensitive", UNSET)

        scorer_multimodal_capabilities_filter = cls(
            operator=operator, value=value, name=name, case_sensitive=case_sensitive
        )

        scorer_multimodal_capabilities_filter.additional_properties = d
        return scorer_multimodal_capabilities_filter

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
