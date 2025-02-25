from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_version_index_sort import DatasetVersionIndexSort


T = TypeVar("T", bound="ListDatasetVersionParams")


@_attrs_define
class ListDatasetVersionParams:
    """
    Attributes:
        sort (Union['DatasetVersionIndexSort', None, Unset]):
    """

    sort: Union["DatasetVersionIndexSort", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_version_index_sort import DatasetVersionIndexSort

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, DatasetVersionIndexSort):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.dataset_version_index_sort import DatasetVersionIndexSort

        d = src_dict.copy()

        def _parse_sort(data: object) -> Union["DatasetVersionIndexSort", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0 = DatasetVersionIndexSort.from_dict(data)

                return sort_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatasetVersionIndexSort", None, Unset], data)

        sort = _parse_sort(d.pop("sort", UNSET))

        list_dataset_version_params = cls(sort=sort)

        list_dataset_version_params.additional_properties = d
        return list_dataset_version_params

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
