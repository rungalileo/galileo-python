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
    Attributes
    ----------
        id (str): Column id.  Must be universally unique.
        category (ColumnCategory):
        data_type (Union[DataType, None]): Data type of the column. This is used to determine how to format the data on
            the UI.
        label (Union[None, Unset, str]): Display label of the column in the UI.
        description (Union[None, Unset, str]): Description of the column.
        group_label (Union[None, Unset, str]): Display label of the column group.
        data_unit (Union[DataUnit, None, Unset]): Data unit of the column (optional).
        multi_valued (Union[Unset, bool]): Whether the column is multi-valued. Default: False.
        allowed_values (Union[None, Unset, list[Any]]): Allowed values for this column.
        sortable (Union[Unset, bool]): Whether the column is sortable.
        filterable (Union[Unset, bool]): Whether the column is filterable.
        is_empty (Union[Unset, bool]): Indicates whether the column is empty and should be hidden. Default: False.
        applicable_types (Union[Unset, list[StepType]]): List of types applicable for this column.
        complex_ (Union[Unset, bool]): Whether the column requires special handling in the UI. Setting this to True will
            hide the column in the UI until the UI adds support for it. Default: False.
        is_optional (Union[Unset, bool]): Whether the column is optional. Default: False.
        roll_up_method (Union[None, Unset, str]): Default roll-up aggregation method for this metric (e.g., 'sum',
            'average').
    """

    id: str
    category: ColumnCategory
    data_type: DataType | None
    label: None | Unset | str = UNSET
    description: None | Unset | str = UNSET
    group_label: None | Unset | str = UNSET
    data_unit: DataUnit | None | Unset = UNSET
    multi_valued: Unset | bool = False
    allowed_values: None | Unset | list[Any] = UNSET
    sortable: Unset | bool = UNSET
    filterable: Unset | bool = UNSET
    is_empty: Unset | bool = False
    applicable_types: Unset | list[StepType] = UNSET
    complex_: Unset | bool = False
    is_optional: Unset | bool = False
    roll_up_method: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        category = self.category.value

        data_type: None | str
        data_type = self.data_type.value if isinstance(self.data_type, DataType) else self.data_type

        label: None | Unset | str
        label = UNSET if isinstance(self.label, Unset) else self.label

        description: None | Unset | str
        description = UNSET if isinstance(self.description, Unset) else self.description

        group_label: None | Unset | str
        group_label = UNSET if isinstance(self.group_label, Unset) else self.group_label

        data_unit: None | Unset | str
        if isinstance(self.data_unit, Unset):
            data_unit = UNSET
        elif isinstance(self.data_unit, DataUnit):
            data_unit = self.data_unit.value
        else:
            data_unit = self.data_unit

        multi_valued = self.multi_valued

        allowed_values: None | Unset | list[Any]
        if isinstance(self.allowed_values, Unset):
            allowed_values = UNSET
        elif isinstance(self.allowed_values, list):
            allowed_values = self.allowed_values

        else:
            allowed_values = self.allowed_values

        sortable = self.sortable

        filterable = self.filterable

        is_empty = self.is_empty

        applicable_types: Unset | list[str] = UNSET
        if not isinstance(self.applicable_types, Unset):
            applicable_types = []
            for applicable_types_item_data in self.applicable_types:
                applicable_types_item = applicable_types_item_data.value
                applicable_types.append(applicable_types_item)

        complex_ = self.complex_

        is_optional = self.is_optional

        roll_up_method: None | Unset | str
        roll_up_method = UNSET if isinstance(self.roll_up_method, Unset) else self.roll_up_method

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
                return DataType(data)

            except:  # noqa: E722
                pass
            return cast(DataType | None, data)

        data_type = _parse_data_type(d.pop("data_type"))

        def _parse_label(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_description(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_group_label(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        group_label = _parse_group_label(d.pop("group_label", UNSET))

        def _parse_data_unit(data: object) -> DataUnit | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return DataUnit(data)

            except:  # noqa: E722
                pass
            return cast(DataUnit | None | Unset, data)

        data_unit = _parse_data_unit(d.pop("data_unit", UNSET))

        multi_valued = d.pop("multi_valued", UNSET)

        def _parse_allowed_values(data: object) -> None | Unset | list[Any]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[Any], data)

            except:  # noqa: E722
                pass
            return cast(None | Unset | list[Any], data)

        allowed_values = _parse_allowed_values(d.pop("allowed_values", UNSET))

        sortable = d.pop("sortable", UNSET)

        filterable = d.pop("filterable", UNSET)

        is_empty = d.pop("is_empty", UNSET)

        applicable_types = []
        _applicable_types = d.pop("applicable_types", UNSET)
        for applicable_types_item_data in _applicable_types or []:
            applicable_types_item = StepType(applicable_types_item_data)

            applicable_types.append(applicable_types_item)

        complex_ = d.pop("complex", UNSET)

        is_optional = d.pop("is_optional", UNSET)

        def _parse_roll_up_method(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

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
