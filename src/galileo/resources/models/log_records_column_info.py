from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.column_category import ColumnCategory
from ..models.data_type import DataType
from ..models.data_unit import DataUnit
from ..models.insight_type import InsightType
from ..models.log_records_column_info_label_color_type_0 import LogRecordsColumnInfoLabelColorType0
from ..models.log_records_filter_type import LogRecordsFilterType
from ..models.step_type import StepType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_threshold import MetricThreshold
    from ..models.scorer_config import ScorerConfig


T = TypeVar("T", bound="LogRecordsColumnInfo")


@_attrs_define
class LogRecordsColumnInfo:
    """
    Attributes
    ----------
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
        scorer_config (None | ScorerConfig | Unset): For metric columns only: Scorer config that produced the metric.
        scorer_id (None | str | Unset): For metric columns only: Scorer id that produced the metric. This is deprecated
            and will be removed in future versions.
        insight_type (InsightType | None | Unset): Insight type.
        filter_type (LogRecordsFilterType | None | Unset): Filter type.
        threshold (MetricThreshold | None | Unset): Thresholds for the column, if this is a metrics column.
        label_color (LogRecordsColumnInfoLabelColorType0 | None | Unset): Type of label color for the column, if this is
            a multilabel metric column.
        metric_key_alias (None | str | Unset): Alternate metric key for this column. When store_metric_ids is ON, this
            holds the legacy metric_name string. Used for dual-key ClickHouse queries.
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
    scorer_config: None | ScorerConfig | Unset = UNSET
    scorer_id: None | str | Unset = UNSET
    insight_type: InsightType | None | Unset = UNSET
    filter_type: LogRecordsFilterType | None | Unset = UNSET
    threshold: MetricThreshold | None | Unset = UNSET
    label_color: LogRecordsColumnInfoLabelColorType0 | None | Unset = UNSET
    metric_key_alias: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_threshold import MetricThreshold
        from ..models.scorer_config import ScorerConfig

        id = self.id

        category = self.category.value

        data_type: None | str
        data_type = self.data_type.value if isinstance(self.data_type, DataType) else self.data_type

        label: None | str | Unset
        label = UNSET if isinstance(self.label, Unset) else self.label

        description: None | str | Unset
        description = UNSET if isinstance(self.description, Unset) else self.description

        group_label: None | str | Unset
        group_label = UNSET if isinstance(self.group_label, Unset) else self.group_label

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
        roll_up_method = UNSET if isinstance(self.roll_up_method, Unset) else self.roll_up_method

        scorer_config: dict[str, Any] | None | Unset
        if isinstance(self.scorer_config, Unset):
            scorer_config = UNSET
        elif isinstance(self.scorer_config, ScorerConfig):
            scorer_config = self.scorer_config.to_dict()
        else:
            scorer_config = self.scorer_config

        scorer_id: None | str | Unset
        scorer_id = UNSET if isinstance(self.scorer_id, Unset) else self.scorer_id

        insight_type: None | str | Unset
        if isinstance(self.insight_type, Unset):
            insight_type = UNSET
        elif isinstance(self.insight_type, InsightType):
            insight_type = self.insight_type.value
        else:
            insight_type = self.insight_type

        filter_type: None | str | Unset
        if isinstance(self.filter_type, Unset):
            filter_type = UNSET
        elif isinstance(self.filter_type, LogRecordsFilterType):
            filter_type = self.filter_type.value
        else:
            filter_type = self.filter_type

        threshold: dict[str, Any] | None | Unset
        if isinstance(self.threshold, Unset):
            threshold = UNSET
        elif isinstance(self.threshold, MetricThreshold):
            threshold = self.threshold.to_dict()
        else:
            threshold = self.threshold

        label_color: None | str | Unset
        if isinstance(self.label_color, Unset):
            label_color = UNSET
        elif isinstance(self.label_color, LogRecordsColumnInfoLabelColorType0):
            label_color = self.label_color.value
        else:
            label_color = self.label_color

        metric_key_alias: None | str | Unset
        metric_key_alias = UNSET if isinstance(self.metric_key_alias, Unset) else self.metric_key_alias

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
        if scorer_config is not UNSET:
            field_dict["scorer_config"] = scorer_config
        if scorer_id is not UNSET:
            field_dict["scorer_id"] = scorer_id
        if insight_type is not UNSET:
            field_dict["insight_type"] = insight_type
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if threshold is not UNSET:
            field_dict["threshold"] = threshold
        if label_color is not UNSET:
            field_dict["label_color"] = label_color
        if metric_key_alias is not UNSET:
            field_dict["metric_key_alias"] = metric_key_alias

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_threshold import MetricThreshold
        from ..models.scorer_config import ScorerConfig

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
                return DataUnit(data)

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
                return cast(list[Any], data)

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

        def _parse_scorer_config(data: object) -> None | ScorerConfig | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ScorerConfig.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | ScorerConfig | Unset, data)

        scorer_config = _parse_scorer_config(d.pop("scorer_config", UNSET))

        def _parse_scorer_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scorer_id = _parse_scorer_id(d.pop("scorer_id", UNSET))

        def _parse_insight_type(data: object) -> InsightType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return InsightType(data)

            except:  # noqa: E722
                pass
            return cast(InsightType | None | Unset, data)

        insight_type = _parse_insight_type(d.pop("insight_type", UNSET))

        def _parse_filter_type(data: object) -> LogRecordsFilterType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return LogRecordsFilterType(data)

            except:  # noqa: E722
                pass
            return cast(LogRecordsFilterType | None | Unset, data)

        filter_type = _parse_filter_type(d.pop("filter_type", UNSET))

        def _parse_threshold(data: object) -> MetricThreshold | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MetricThreshold.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(MetricThreshold | None | Unset, data)

        threshold = _parse_threshold(d.pop("threshold", UNSET))

        def _parse_label_color(data: object) -> LogRecordsColumnInfoLabelColorType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return LogRecordsColumnInfoLabelColorType0(data)

            except:  # noqa: E722
                pass
            return cast(LogRecordsColumnInfoLabelColorType0 | None | Unset, data)

        label_color = _parse_label_color(d.pop("label_color", UNSET))

        def _parse_metric_key_alias(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metric_key_alias = _parse_metric_key_alias(d.pop("metric_key_alias", UNSET))

        log_records_column_info = cls(
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
            scorer_config=scorer_config,
            scorer_id=scorer_id,
            insight_type=insight_type,
            filter_type=filter_type,
            threshold=threshold,
            label_color=label_color,
            metric_key_alias=metric_key_alias,
        )

        log_records_column_info.additional_properties = d
        return log_records_column_info

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
