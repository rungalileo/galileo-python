from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.column_category import ColumnCategory
from ..models.data_type import DataType
from ..models.data_unit import DataUnit
from ..models.step_type import StepType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ColumnInfo")


@_attrs_define
class ColumnInfo:
    """
    Attributes:
        id (str): Column id.  Must be universally unique.
        category (ColumnCategory):
        data_type (DataType | None): Data type of the column. This is used to determine how to format the data on the
            UI.
        label (None | str | Unset): Display label of the column in the UI.
        description (None | str | Unset): Description of the column.
        group_label (None | str | Unset): Display label of the column group.
        data_unit (DataUnit | None | Unset): Data unit of the column (optional).
        multi_valued (bool | Unset): Whether the column is multi-valued. Default: False.
        allowed_values (list[Any] | None | Unset): Allowed values for this column.
        sortable (bool | Unset): Whether the column is sortable.
        filterable (bool | Unset): Whether the column is filterable.
        is_empty (bool | Unset): Indicates whether the column is empty and should be hidden. Default: False.
        applicable_types (list[StepType] | Unset): List of types applicable for this column.
        complex_ (bool | Unset): Whether the column requires special handling in the UI. Setting this to True will hide
            the column in the UI until the UI adds support for it. Default: False.
        is_optional (bool | Unset): Whether the column is optional. Default: False.
        roll_up_method (None | str | Unset): Default roll-up aggregation method for this metric (e.g., 'sum',
            'average').
    """

    id: str
    category: ColumnCategory
    data_type: DataType | None
    label: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    group_label: None | str | Unset = UNSET
    data_unit: DataUnit | None | Unset = UNSET
    multi_valued: bool | Unset = False
    allowed_values: list[Any] | None | Unset = UNSET
    sortable: bool | Unset = UNSET
    filterable: bool | Unset = UNSET
    is_empty: bool | Unset = False
    applicable_types: list[StepType] | Unset = UNSET
    complex_: bool | Unset = False
    is_optional: bool | Unset = False
    roll_up_method: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        category = self.category.value

        data_type: None | str
        if isinstance(self.data_type, DataType):
            data_type = self.data_type.value
        else:
            data_type = self.data_type

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        group_label: None | str | Unset
        if isinstance(self.group_label, Unset):
            group_label = UNSET
        else:
            group_label = self.group_label

        data_unit: None | str | Unset
        if isinstance(self.data_unit, Unset):
            data_unit = UNSET
        elif isinstance(self.data_unit, DataUnit):
            data_unit = self.data_unit.value
        else:
            data_unit = self.data_unit

        multi_valued = self.multi_valued

        allowed_values: list[Any] | None | Unset
        if isinstance(self.allowed_values, Unset):
            allowed_values = UNSET
        elif isinstance(self.allowed_values, list):
            allowed_values = self.allowed_values

        else:
            allowed_values = self.allowed_values

        sortable = self.sortable

        filterable = self.filterable

        is_empty = self.is_empty

        applicable_types: list[str] | Unset = UNSET
        if not isinstance(self.applicable_types, Unset):
            applicable_types = []
            for applicable_types_item_data in self.applicable_types:
                applicable_types_item = applicable_types_item_data.value
                applicable_types.append(applicable_types_item)

        complex_ = self.complex_

        is_optional = self.is_optional

        roll_up_method: None | str | Unset
        if isinstance(self.roll_up_method, Unset):
            roll_up_method = UNSET
        else:
            roll_up_method = self.roll_up_method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "category": category, "data_type": data_type})
        if label is not UNSET:
            field_dict["label"] = label
        if description is not UNSET:
            field_dict["description"] = description
        if group_label is not UNSET:
            field_dict["group_label"] = group_label
        if data_unit is not UNSET:
            field_dict["data_unit"] = data_unit
        if multi_valued is not UNSET:
            field_dict["multi_valued"] = multi_valued
        if allowed_values is not UNSET:
            field_dict["allowed_values"] = allowed_values
        if sortable is not UNSET:
            field_dict["sortable"] = sortable
        if filterable is not UNSET:
            field_dict["filterable"] = filterable
        if is_empty is not UNSET:
            field_dict["is_empty"] = is_empty
        if applicable_types is not UNSET:
            field_dict["applicable_types"] = applicable_types
        if complex_ is not UNSET:
            field_dict["complex"] = complex_
        if is_optional is not UNSET:
            field_dict["is_optional"] = is_optional
        if roll_up_method is not UNSET:
            field_dict["roll_up_method"] = roll_up_method

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        category = ColumnCategory(d.pop("category"))

        def _parse_data_type(data: object) -> DataType | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                data_type_type_0 = DataType(data)

                return data_type_type_0
            except:  # noqa: E722
                pass
            return cast(DataType | None, data)

        data_type = _parse_data_type(d.pop("data_type"))

        def _parse_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_group_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_label = _parse_group_label(d.pop("group_label", UNSET))

        def _parse_data_unit(data: object) -> DataUnit | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                data_unit_type_0 = DataUnit(data)

                return data_unit_type_0
            except:  # noqa: E722
                pass
            return cast(DataUnit | None | Unset, data)

        data_unit = _parse_data_unit(d.pop("data_unit", UNSET))

        multi_valued = d.pop("multi_valued", UNSET)

        def _parse_allowed_values(data: object) -> list[Any] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_values_type_0 = cast(list[Any], data)

                return allowed_values_type_0
            except:  # noqa: E722
                pass
            return cast(list[Any] | None | Unset, data)

        allowed_values = _parse_allowed_values(d.pop("allowed_values", UNSET))

        sortable = d.pop("sortable", UNSET)

        filterable = d.pop("filterable", UNSET)

        is_empty = d.pop("is_empty", UNSET)

        _applicable_types = d.pop("applicable_types", UNSET)
        applicable_types: list[StepType] | Unset = UNSET
        if _applicable_types is not UNSET:
            applicable_types = []
            for applicable_types_item_data in _applicable_types:
                applicable_types_item = StepType(applicable_types_item_data)

                applicable_types.append(applicable_types_item)

        complex_ = d.pop("complex", UNSET)

        is_optional = d.pop("is_optional", UNSET)

        def _parse_roll_up_method(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        roll_up_method = _parse_roll_up_method(d.pop("roll_up_method", UNSET))

        column_info = cls(
            id=id,
            category=category,
            data_type=data_type,
            label=label,
            description=description,
            group_label=group_label,
            data_unit=data_unit,
            multi_valued=multi_valued,
            allowed_values=allowed_values,
            sortable=sortable,
            filterable=filterable,
            is_empty=is_empty,
            applicable_types=applicable_types,
            complex_=complex_,
            is_optional=is_optional,
            roll_up_method=roll_up_method,
        )

        column_info.additional_properties = d
        return column_info

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
