from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metadata_filter_operator import MetadataFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataFilter")


@_attrs_define
class MetadataFilter:
    """Filters on metadata key-value pairs in scorer jobs.

    Attributes
    ----------
        operator (MetadataFilterOperator):
        key (str):
        value (Union[list[str], str]):
        name (Union[Literal['metadata'], Unset]):  Default: 'metadata'.
        filter_type (Union[Literal['map'], Unset]):  Default: 'map'.
    """

    operator: MetadataFilterOperator
    key: str
    value: Union[list[str], str]
    name: Union[Literal["metadata"], Unset] = "metadata"
    filter_type: Union[Literal["map"], Unset] = "map"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        key = self.key

        value: Union[list[str], str]
        value = self.value if isinstance(self.value, list) else self.value

        name = self.name

        filter_type = self.filter_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "key": key, "value": value})
        if name is not UNSET:
            field_dict["name"] = name
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operator = MetadataFilterOperator(d.pop("operator"))

        key = d.pop("key")

        def _parse_value(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["metadata"], Unset], d.pop("name", UNSET))
        if name != "metadata" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'metadata', got '{name}'")

        filter_type = cast(Union[Literal["map"], Unset], d.pop("filter_type", UNSET))
        if filter_type != "map" and not isinstance(filter_type, Unset):
            raise ValueError(f"filter_type must match const 'map', got '{filter_type}'")

        metadata_filter = cls(operator=operator, key=key, value=value, name=name, filter_type=filter_type)

        metadata_filter.additional_properties = d
        return metadata_filter

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
