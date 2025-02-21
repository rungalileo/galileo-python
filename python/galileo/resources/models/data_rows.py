from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.data_row import DataRow


T = TypeVar("T", bound="DataRows")


@_attrs_define
class DataRows:
    """
    Attributes:
        data_rows (list['DataRow']):
        has_next_page (bool):
    """

    data_rows: list["DataRow"]
    has_next_page: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_rows = []
        for data_rows_item_data in self.data_rows:
            data_rows_item = data_rows_item_data.to_dict()
            data_rows.append(data_rows_item)

        has_next_page = self.has_next_page

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"data_rows": data_rows, "has_next_page": has_next_page})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.data_row import DataRow

        d = src_dict.copy()
        data_rows = []
        _data_rows = d.pop("data_rows")
        for data_rows_item_data in _data_rows:
            data_rows_item = DataRow.from_dict(data_rows_item_data)

            data_rows.append(data_rows_item)

        has_next_page = d.pop("has_next_page")

        data_rows = cls(data_rows=data_rows, has_next_page=has_next_page)

        data_rows.additional_properties = d
        return data_rows

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
