from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.column_category import ColumnCategory
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_threshold import MetricThreshold


T = TypeVar("T", bound="LogDataColumnInfo")


@_attrs_define
class LogDataColumnInfo:
    """
    Attributes:
        category (ColumnCategory):
        id (str): Unique identifier of the column.  Format is subject to change and should not be used/parsed directly.
        data_type (Union[Unset, Any]): Data type of the column. This is used to determine how to format the data on the
            UI. Default: 'unknown'.
        description (Union[None, Unset, str]): Description of the column.
        filterable (Union[Unset, bool]): Whether the column is filterable by value. Doesn't include categorical filters
            Default: True.
        group_description (Union[None, Unset, str]): Description of the group (super column).
        group_label (Union[None, Unset, str]): Display label of the group (super column) in the UI.
        label (Union[None, Unset, str]): Display label of the column in the UI.
        sortable (Union[Unset, bool]): Whether the column is sortable. Default: True.
        threshold (Union['MetricThreshold', None, Unset]): Thresholds for the column, if this is a metrics column.
    """

    category: ColumnCategory
    id: str
    data_type: Union[Unset, Any] = "unknown"
    description: Union[None, Unset, str] = UNSET
    filterable: Union[Unset, bool] = True
    group_description: Union[None, Unset, str] = UNSET
    group_label: Union[None, Unset, str] = UNSET
    label: Union[None, Unset, str] = UNSET
    sortable: Union[Unset, bool] = True
    threshold: Union["MetricThreshold", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_threshold import MetricThreshold

        category = self.category.value

        id = self.id

        data_type = self.data_type

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        filterable = self.filterable

        group_description: Union[None, Unset, str]
        if isinstance(self.group_description, Unset):
            group_description = UNSET
        else:
            group_description = self.group_description

        group_label: Union[None, Unset, str]
        if isinstance(self.group_label, Unset):
            group_label = UNSET
        else:
            group_label = self.group_label

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        sortable = self.sortable

        threshold: Union[None, Unset, dict[str, Any]]
        if isinstance(self.threshold, Unset):
            threshold = UNSET
        elif isinstance(self.threshold, MetricThreshold):
            threshold = self.threshold.to_dict()
        else:
            threshold = self.threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"category": category, "id": id})
        if data_type is not UNSET:
            field_dict["data_type"] = data_type
        if description is not UNSET:
            field_dict["description"] = description
        if filterable is not UNSET:
            field_dict["filterable"] = filterable
        if group_description is not UNSET:
            field_dict["group_description"] = group_description
        if group_label is not UNSET:
            field_dict["group_label"] = group_label
        if label is not UNSET:
            field_dict["label"] = label
        if sortable is not UNSET:
            field_dict["sortable"] = sortable
        if threshold is not UNSET:
            field_dict["threshold"] = threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric_threshold import MetricThreshold

        d = src_dict.copy()
        category = ColumnCategory(d.pop("category"))

        id = d.pop("id")

        data_type = d.pop("data_type", UNSET)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        filterable = d.pop("filterable", UNSET)

        def _parse_group_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_description = _parse_group_description(d.pop("group_description", UNSET))

        def _parse_group_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_label = _parse_group_label(d.pop("group_label", UNSET))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        sortable = d.pop("sortable", UNSET)

        def _parse_threshold(data: object) -> Union["MetricThreshold", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                threshold_type_0 = MetricThreshold.from_dict(data)

                return threshold_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MetricThreshold", None, Unset], data)

        threshold = _parse_threshold(d.pop("threshold", UNSET))

        log_data_column_info = cls(
            category=category,
            id=id,
            data_type=data_type,
            description=description,
            filterable=filterable,
            group_description=group_description,
            group_label=group_label,
            label=label,
            sortable=sortable,
            threshold=threshold,
        )

        log_data_column_info.additional_properties = d
        return log_data_column_info

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
