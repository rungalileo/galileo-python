from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DatasetRow")


@_attrs_define
class DatasetRow:
    """
    Attributes:
        index (int):
        values (list[Union[None, float, int, str]]):
    """

    index: int
    values: list[Union[None, float, int, str]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        values = []
        for values_item_data in self.values:
            values_item: Union[None, float, int, str]
            values_item = values_item_data
            values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"index": index, "values": values})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        index = d.pop("index")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:

            def _parse_values_item(data: object) -> Union[None, float, int, str]:
                if data is None:
                    return data
                return cast(Union[None, float, int, str], data)

            values_item = _parse_values_item(values_item_data)

            values.append(values_item)

        dataset_row = cls(index=index, values=values)

        dataset_row.additional_properties = d
        return dataset_row

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
