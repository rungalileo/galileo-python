from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.boolean_filter import BooleanFilter
    from ..models.collection_filter import CollectionFilter
    from ..models.custom_boolean_filter import CustomBooleanFilter
    from ..models.custom_function_filter import CustomFunctionFilter
    from ..models.custom_number_filter import CustomNumberFilter
    from ..models.custom_uuid_filter import CustomUUIDFilter
    from ..models.date_filter import DateFilter
    from ..models.enum_filter import EnumFilter
    from ..models.id_filter import IDFilter
    from ..models.map_filter import MapFilter
    from ..models.string_filter import StringFilter


T = TypeVar("T", bound="FilterLeaf")


@_attrs_define
class FilterLeaf:
    """
    Attributes:
        filter_ (Union['BooleanFilter', 'CollectionFilter', 'CustomBooleanFilter', 'CustomFunctionFilter',
            'CustomNumberFilter', 'CustomUUIDFilter', 'DateFilter', 'EnumFilter', 'IDFilter', 'MapFilter', 'StringFilter']):
    """

    filter_: Union[
        "BooleanFilter",
        "CollectionFilter",
        "CustomBooleanFilter",
        "CustomFunctionFilter",
        "CustomNumberFilter",
        "CustomUUIDFilter",
        "DateFilter",
        "EnumFilter",
        "IDFilter",
        "MapFilter",
        "StringFilter",
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.boolean_filter import BooleanFilter
        from ..models.collection_filter import CollectionFilter
        from ..models.custom_boolean_filter import CustomBooleanFilter
        from ..models.custom_number_filter import CustomNumberFilter
        from ..models.custom_uuid_filter import CustomUUIDFilter
        from ..models.date_filter import DateFilter
        from ..models.enum_filter import EnumFilter
        from ..models.id_filter import IDFilter
        from ..models.map_filter import MapFilter
        from ..models.string_filter import StringFilter

        filter_: dict[str, Any]
        if isinstance(
            self.filter_,
            (
                IDFilter,
                CustomUUIDFilter,
                DateFilter,
                BooleanFilter,
                CustomNumberFilter,
                EnumFilter,
                MapFilter,
                CollectionFilter,
                StringFilter,
                CustomBooleanFilter,
            ),
        ):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"filter": filter_})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.boolean_filter import BooleanFilter
        from ..models.collection_filter import CollectionFilter
        from ..models.custom_boolean_filter import CustomBooleanFilter
        from ..models.custom_function_filter import CustomFunctionFilter
        from ..models.custom_number_filter import CustomNumberFilter
        from ..models.custom_uuid_filter import CustomUUIDFilter
        from ..models.date_filter import DateFilter
        from ..models.enum_filter import EnumFilter
        from ..models.id_filter import IDFilter
        from ..models.map_filter import MapFilter
        from ..models.string_filter import StringFilter

        d = dict(src_dict)

        def _parse_filter_(
            data: object,
        ) -> Union[
            "BooleanFilter",
            "CollectionFilter",
            "CustomBooleanFilter",
            "CustomFunctionFilter",
            "CustomNumberFilter",
            "CustomUUIDFilter",
            "DateFilter",
            "EnumFilter",
            "IDFilter",
            "MapFilter",
            "StringFilter",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return IDFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomUUIDFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return DateFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BooleanFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomNumberFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return EnumFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MapFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CollectionFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return StringFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomBooleanFilter.from_dict(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            return CustomFunctionFilter.from_dict(data)

        filter_ = _parse_filter_(d.pop("filter"))

        filter_leaf = cls(filter_=filter_)

        filter_leaf.additional_properties = d
        return filter_leaf

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
