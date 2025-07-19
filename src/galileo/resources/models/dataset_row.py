from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dataset_row_metadata import DatasetRowMetadata
    from ..models.dataset_row_values_dict import DatasetRowValuesDict


T = TypeVar("T", bound="DatasetRow")


@_attrs_define
class DatasetRow:
    """
    Attributes:
        index (int):
        metadata (Union['DatasetRowMetadata', None]):
        row_id (str):
        values (list[Union[None, float, int, str]]):
        values_dict (DatasetRowValuesDict):
    """

    index: int
    metadata: Union["DatasetRowMetadata", None]
    row_id: str
    values: list[Union[None, float, int, str]]
    values_dict: "DatasetRowValuesDict"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_row_metadata import DatasetRowMetadata

        index = self.index

        metadata: Union[None, dict[str, Any]]
        if isinstance(self.metadata, DatasetRowMetadata):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        row_id = self.row_id

        values = []
        for values_item_data in self.values:
            values_item: Union[None, float, int, str]
            values_item = values_item_data
            values.append(values_item)

        values_dict = self.values_dict.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"index": index, "metadata": metadata, "row_id": row_id, "values": values, "values_dict": values_dict}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_row_metadata import DatasetRowMetadata
        from ..models.dataset_row_values_dict import DatasetRowValuesDict

        d = dict(src_dict)
        index = d.pop("index")

        def _parse_metadata(data: object) -> Union["DatasetRowMetadata", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = DatasetRowMetadata.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatasetRowMetadata", None], data)

        metadata = _parse_metadata(d.pop("metadata"))

        row_id = d.pop("row_id")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:

            def _parse_values_item(data: object) -> Union[None, float, int, str]:
                if data is None:
                    return data
                return cast(Union[None, float, int, str], data)

            values_item = _parse_values_item(values_item_data)

            values.append(values_item)

        values_dict = DatasetRowValuesDict.from_dict(d.pop("values_dict"))

        dataset_row = cls(index=index, metadata=metadata, row_id=row_id, values=values, values_dict=values_dict)

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
