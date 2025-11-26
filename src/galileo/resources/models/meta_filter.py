from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetaFilter")


@_attrs_define
class MetaFilter:
    """A class for filtering arbitrary metadata columns.

    Attributes
    ----------
        name (str):
        greater_than (Union[None, Unset, float]):
        less_than (Union[None, Unset, float]):
        isin (Union[None, Unset, list[Union[None, bool, int, str]]]):
        is_equal (Union[None, Unset, float, int]):
    """

    name: str
    greater_than: Union[None, Unset, float] = UNSET
    less_than: Union[None, Unset, float] = UNSET
    isin: Union[None, Unset, list[Union[None, bool, int, str]]] = UNSET
    is_equal: Union[None, Unset, float, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        greater_than: Union[None, Unset, float]
        greater_than = UNSET if isinstance(self.greater_than, Unset) else self.greater_than

        less_than: Union[None, Unset, float]
        less_than = UNSET if isinstance(self.less_than, Unset) else self.less_than

        isin: Union[None, Unset, list[Union[None, bool, int, str]]]
        if isinstance(self.isin, Unset):
            isin = UNSET
        elif isinstance(self.isin, list):
            isin = []
            for isin_type_0_item_data in self.isin:
                isin_type_0_item: Union[None, bool, int, str]
                isin_type_0_item = isin_type_0_item_data
                isin.append(isin_type_0_item)

        else:
            isin = self.isin

        is_equal: Union[None, Unset, float, int]
        is_equal = UNSET if isinstance(self.is_equal, Unset) else self.is_equal

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if greater_than is not UNSET:
            field_dict["greater_than"] = greater_than
        if less_than is not UNSET:
            field_dict["less_than"] = less_than
        if isin is not UNSET:
            field_dict["isin"] = isin
        if is_equal is not UNSET:
            field_dict["is_equal"] = is_equal

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_greater_than(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        greater_than = _parse_greater_than(d.pop("greater_than", UNSET))

        def _parse_less_than(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        less_than = _parse_less_than(d.pop("less_than", UNSET))

        def _parse_isin(data: object) -> Union[None, Unset, list[Union[None, bool, int, str]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                isin_type_0 = []
                _isin_type_0 = data
                for isin_type_0_item_data in _isin_type_0:

                    def _parse_isin_type_0_item(data: object) -> Union[None, bool, int, str]:
                        if data is None:
                            return data
                        return cast(Union[None, bool, int, str], data)

                    isin_type_0_item = _parse_isin_type_0_item(isin_type_0_item_data)

                    isin_type_0.append(isin_type_0_item)

                return isin_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Union[None, bool, int, str]]], data)

        isin = _parse_isin(d.pop("isin", UNSET))

        def _parse_is_equal(data: object) -> Union[None, Unset, float, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float, int], data)

        is_equal = _parse_is_equal(d.pop("is_equal", UNSET))

        meta_filter = cls(name=name, greater_than=greater_than, less_than=less_than, isin=isin, is_equal=is_equal)

        meta_filter.additional_properties = d
        return meta_filter

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
