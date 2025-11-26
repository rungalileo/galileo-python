from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dataset_row_metadata import DatasetRowMetadata
    from ..models.dataset_row_values_dict import DatasetRowValuesDict
    from ..models.dataset_row_values_item_type_3 import DatasetRowValuesItemType3


T = TypeVar("T", bound="DatasetRow")


@_attrs_define
class DatasetRow:
    """
    Attributes
    ----------
        row_id (str):
        index (int):
        values (list[Union['DatasetRowValuesItemType3', None, float, int, str]]):
        values_dict (DatasetRowValuesDict):
        metadata (Union['DatasetRowMetadata', None]):
    """

    row_id: str
    index: int
    values: list[Union["DatasetRowValuesItemType3", None, float, int, str]]
    values_dict: "DatasetRowValuesDict"
    metadata: Union["DatasetRowMetadata", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_row_metadata import DatasetRowMetadata
        from ..models.dataset_row_values_item_type_3 import DatasetRowValuesItemType3

        row_id = self.row_id

        index = self.index

        values = []
        for values_item_data in self.values:
            values_item: Union[None, dict[str, Any], float, int, str]
            if isinstance(values_item_data, DatasetRowValuesItemType3):
                values_item = values_item_data.to_dict()
            else:
                values_item = values_item_data
            values.append(values_item)

        values_dict = self.values_dict.to_dict()

        metadata: Union[None, dict[str, Any]]
        metadata = self.metadata.to_dict() if isinstance(self.metadata, DatasetRowMetadata) else self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"row_id": row_id, "index": index, "values": values, "values_dict": values_dict, "metadata": metadata}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_row_metadata import DatasetRowMetadata
        from ..models.dataset_row_values_dict import DatasetRowValuesDict
        from ..models.dataset_row_values_item_type_3 import DatasetRowValuesItemType3

        d = dict(src_dict)
        row_id = d.pop("row_id")

        index = d.pop("index")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:

            def _parse_values_item(data: object) -> Union["DatasetRowValuesItemType3", None, float, int, str]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return DatasetRowValuesItemType3.from_dict(data)

                except:  # noqa: E722
                    pass
                return cast(Union["DatasetRowValuesItemType3", None, float, int, str], data)

            values_item = _parse_values_item(values_item_data)

            values.append(values_item)

        values_dict = DatasetRowValuesDict.from_dict(d.pop("values_dict"))

        def _parse_metadata(data: object) -> Union["DatasetRowMetadata", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return DatasetRowMetadata.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["DatasetRowMetadata", None], data)

        metadata = _parse_metadata(d.pop("metadata"))

        dataset_row = cls(row_id=row_id, index=index, values=values, values_dict=values_dict, metadata=metadata)

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
