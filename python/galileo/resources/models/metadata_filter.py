from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metadata_filter_operator import MetadataFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataFilter")


@_attrs_define
class MetadataFilter:
    """Filters on metadata key-value pairs in scorer jobs.

    Attributes:
        key (str):
        operator (MetadataFilterOperator):
        value (Union[list[str], str]):
        filter_type (Union[Literal['map'], Unset]):  Default: 'map'.
        name (Union[Literal['metadata'], Unset]):  Default: 'metadata'.
    """

    key: str
    operator: MetadataFilterOperator
    value: Union[list[str], str]
    filter_type: Union[Literal["map"], Unset] = "map"
    name: Union[Literal["metadata"], Unset] = "metadata"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        operator = self.operator.value

        value: Union[list[str], str]
        if isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        filter_type = self.filter_type

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"key": key, "operator": operator, "value": value})
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        operator = MetadataFilterOperator(d.pop("operator"))

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

        filter_type = cast(Union[Literal["map"], Unset], d.pop("filter_type", UNSET))
        if filter_type != "map" and not isinstance(filter_type, Unset):
            raise ValueError(f"filter_type must match const 'map', got '{filter_type}'")

        name = cast(Union[Literal["metadata"], Unset], d.pop("name", UNSET))
        if name != "metadata" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'metadata', got '{name}'")

        metadata_filter = cls(key=key, operator=operator, value=value, filter_type=filter_type, name=name)

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
