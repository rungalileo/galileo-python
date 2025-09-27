from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dataset_append_row_values_additional_property_type_3 import (
        DatasetAppendRowValuesAdditionalPropertyType3,
    )


T = TypeVar("T", bound="DatasetAppendRowValues")


@_attrs_define
class DatasetAppendRowValues:
    """ """

    additional_properties: dict[str, Union["DatasetAppendRowValuesAdditionalPropertyType3", None, float, int, str]] = (
        _attrs_field(init=False, factory=dict)
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_append_row_values_additional_property_type_3 import (
            DatasetAppendRowValuesAdditionalPropertyType3,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, DatasetAppendRowValuesAdditionalPropertyType3):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_append_row_values_additional_property_type_3 import (
            DatasetAppendRowValuesAdditionalPropertyType3,
        )

        d = dict(src_dict)
        dataset_append_row_values = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union["DatasetAppendRowValuesAdditionalPropertyType3", None, float, int, str]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return DatasetAppendRowValuesAdditionalPropertyType3.from_dict(data)

                except:  # noqa: E722
                    pass
                return cast(Union["DatasetAppendRowValuesAdditionalPropertyType3", None, float, int, str], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        dataset_append_row_values.additional_properties = additional_properties
        return dataset_append_row_values

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union["DatasetAppendRowValuesAdditionalPropertyType3", None, float, int, str]:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: Union["DatasetAppendRowValuesAdditionalPropertyType3", None, float, int, str]
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
