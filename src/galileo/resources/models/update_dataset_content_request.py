from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dataset_append_row import DatasetAppendRow
    from ..models.dataset_delete_row import DatasetDeleteRow
    from ..models.dataset_filter_rows import DatasetFilterRows
    from ..models.dataset_update_row import DatasetUpdateRow


T = TypeVar("T", bound="UpdateDatasetContentRequest")


@_attrs_define
class UpdateDatasetContentRequest:
    """This structure represent the valid edits operations that can be performed on a dataset.
    There edit operations are:
    - Row edits: These edits are performed on a specific row of the dataset.
        - EditMode.id: The edit is performed on the index (numeric index). DEPRECATED
        - EditMode.row_id: The edit is performed on the row_id of the row.
    - Global edits: These edits are performed on the entire dataset and should not be mixed with row edits.
        - EditMode.global_edit

        Attributes:
            edits (list[Union['DatasetAppendRow', 'DatasetDeleteRow', 'DatasetFilterRows', 'DatasetUpdateRow']]):
    """

    edits: list[Union["DatasetAppendRow", "DatasetDeleteRow", "DatasetFilterRows", "DatasetUpdateRow"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_append_row import DatasetAppendRow
        from ..models.dataset_delete_row import DatasetDeleteRow
        from ..models.dataset_update_row import DatasetUpdateRow

        edits = []
        for edits_item_data in self.edits:
            edits_item: dict[str, Any]
            if isinstance(edits_item_data, DatasetAppendRow):
                edits_item = edits_item_data.to_dict()
            elif isinstance(edits_item_data, DatasetUpdateRow):
                edits_item = edits_item_data.to_dict()
            elif isinstance(edits_item_data, DatasetDeleteRow):
                edits_item = edits_item_data.to_dict()
            else:
                edits_item = edits_item_data.to_dict()

            edits.append(edits_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"edits": edits})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_append_row import DatasetAppendRow
        from ..models.dataset_delete_row import DatasetDeleteRow
        from ..models.dataset_filter_rows import DatasetFilterRows
        from ..models.dataset_update_row import DatasetUpdateRow

        d = dict(src_dict)
        edits = []
        _edits = d.pop("edits")
        for edits_item_data in _edits:

            def _parse_edits_item(
                data: object,
            ) -> Union["DatasetAppendRow", "DatasetDeleteRow", "DatasetFilterRows", "DatasetUpdateRow"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    edits_item_type_0 = DatasetAppendRow.from_dict(data)

                    return edits_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    edits_item_type_1 = DatasetUpdateRow.from_dict(data)

                    return edits_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    edits_item_type_2 = DatasetDeleteRow.from_dict(data)

                    return edits_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                edits_item_type_3 = DatasetFilterRows.from_dict(data)

                return edits_item_type_3

            edits_item = _parse_edits_item(edits_item_data)

            edits.append(edits_item)

        update_dataset_content_request = cls(edits=edits)

        update_dataset_content_request.additional_properties = d
        return update_dataset_content_request

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
