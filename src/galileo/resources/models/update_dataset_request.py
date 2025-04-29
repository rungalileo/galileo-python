from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column_mapping import ColumnMapping


T = TypeVar("T", bound="UpdateDatasetRequest")


@_attrs_define
class UpdateDatasetRequest:
    """
    Attributes:
        column_mapping (Union['ColumnMapping', None, Unset]):
        draft (Union[None, Unset, bool]):
        name (Union[None, Unset, str]):
    """

    column_mapping: Union["ColumnMapping", None, Unset] = UNSET
    draft: Union[None, Unset, bool] = UNSET
    name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.column_mapping import ColumnMapping

        column_mapping: Union[None, Unset, dict[str, Any]]
        if isinstance(self.column_mapping, Unset):
            column_mapping = UNSET
        elif isinstance(self.column_mapping, ColumnMapping):
            column_mapping = self.column_mapping.to_dict()
        else:
            column_mapping = self.column_mapping

        draft: Union[None, Unset, bool]
        if isinstance(self.draft, Unset):
            draft = UNSET
        else:
            draft = self.draft

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if column_mapping is not UNSET:
            field_dict["column_mapping"] = column_mapping
        if draft is not UNSET:
            field_dict["draft"] = draft
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.column_mapping import ColumnMapping

        d = src_dict.copy()

        def _parse_column_mapping(data: object) -> Union["ColumnMapping", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                column_mapping_type_0 = ColumnMapping.from_dict(data)

                return column_mapping_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ColumnMapping", None, Unset], data)

        column_mapping = _parse_column_mapping(d.pop("column_mapping", UNSET))

        def _parse_draft(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        draft = _parse_draft(d.pop("draft", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        update_dataset_request = cls(column_mapping=column_mapping, draft=draft, name=name)

        update_dataset_request.additional_properties = d
        return update_dataset_request

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
