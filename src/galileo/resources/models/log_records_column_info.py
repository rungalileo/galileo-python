from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.column_category import ColumnCategory
from ..models.data_type import DataType
from ..models.data_unit import DataUnit
from ..models.insight_type import InsightType
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
        scorer_config (Union['ScorerConfig', None, Unset]): For metric columns only: Scorer config that produced the
            metric.
        scorer_id (Union[None, Unset, str]): For metric columns only: Scorer id that produced the metric. This is
            deprecated and will be removed in future versions.
        insight_type (Union[InsightType, None, Unset]): Insight type.
        filter_type (Union[LogRecordsFilterType, None, Unset]): Filter type.
        threshold (Union['MetricThreshold', None, Unset]): Thresholds for the column, if this is a metrics column.
    """

    id: str
    category: ColumnCategory
    data_type: Union[DataType, None]
    label: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    group_label: Union[None, Unset, str] = UNSET
    data_unit: Union[DataUnit, None, Unset] = UNSET
    multi_valued: Union[Unset, bool] = False
    allowed_values: Union[None, Unset, list[Any]] = UNSET
    sortable: Union[Unset, bool] = UNSET
    filterable: Union[Unset, bool] = UNSET
    is_empty: Union[Unset, bool] = False
    applicable_types: Union[Unset, list[StepType]] = UNSET
    complex_: Union[Unset, bool] = False
    is_optional: Union[Unset, bool] = False
    scorer_config: Union["ScorerConfig", None, Unset] = UNSET
    scorer_id: Union[None, Unset, str] = UNSET
    insight_type: Union[InsightType, None, Unset] = UNSET
    filter_type: Union[LogRecordsFilterType, None, Unset] = UNSET
    threshold: Union["MetricThreshold", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_threshold import MetricThreshold
        from ..models.scorer_config import ScorerConfig

        id = self.id

        category = self.category.value

        data_type: Union[None, str]
        data_type = self.data_type.value if isinstance(self.data_type, DataType) else self.data_type

        label: Union[None, Unset, str]
        label = UNSET if isinstance(self.label, Unset) else self.label

        description: Union[None, Unset, str]
        description = UNSET if isinstance(self.description, Unset) else self.description

        group_label: Union[None, Unset, str]
        group_label = UNSET if isinstance(self.group_label, Unset) else self.group_label

        data_unit: Union[None, Unset, str]
        if isinstance(self.data_unit, Unset):
            data_unit = UNSET
        elif isinstance(self.data_unit, DataUnit):
            data_unit = self.data_unit.value
        else:
            data_unit = self.data_unit

        multi_valued = self.multi_valued

        allowed_values: Union[None, Unset, list[Any]]
        if isinstance(self.allowed_values, Unset):
            allowed_values = UNSET
        elif isinstance(self.allowed_values, list):
            allowed_values = self.allowed_values

        else:
            allowed_values = self.allowed_values

        sortable = self.sortable

        filterable = self.filterable

        is_empty = self.is_empty

        applicable_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.applicable_types, Unset):
            applicable_types = []
            for applicable_types_item_data in self.applicable_types:
                applicable_types_item = applicable_types_item_data.value
                applicable_types.append(applicable_types_item)

        complex_ = self.complex_

        is_optional = self.is_optional

        scorer_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.scorer_config, Unset):
            scorer_config = UNSET
        elif isinstance(self.scorer_config, ScorerConfig):
            scorer_config = self.scorer_config.to_dict()
        else:
            scorer_config = self.scorer_config

        scorer_id: Union[None, Unset, str]
        scorer_id = UNSET if isinstance(self.scorer_id, Unset) else self.scorer_id

        insight_type: Union[None, Unset, str]
        if isinstance(self.insight_type, Unset):
            insight_type = UNSET
        elif isinstance(self.insight_type, InsightType):
            insight_type = self.insight_type.value
        else:
            insight_type = self.insight_type

        filter_type: Union[None, Unset, str]
        if isinstance(self.filter_type, Unset):
            filter_type = UNSET
        elif isinstance(self.filter_type, LogRecordsFilterType):
            filter_type = self.filter_type.value
        else:
            filter_type = self.filter_type

        threshold: Union[None, Unset, dict[str, Any]]
        if isinstance(self.threshold, Unset):
            threshold = UNSET
        elif isinstance(self.threshold, MetricThreshold):
            threshold = self.threshold.to_dict()
        else:
            threshold = self.threshold

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_threshold import MetricThreshold
        from ..models.scorer_config import ScorerConfig

        d = dict(src_dict)
        id = d.pop("id")

        category = ColumnCategory(d.pop("category"))

        def _parse_data_type(data: object) -> Union[DataType, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return DataType(data)

            except:  # noqa: E722
                pass
            return cast(Union[DataType, None], data)

        data_type = _parse_data_type(d.pop("data_type"))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_group_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_label = _parse_group_label(d.pop("group_label", UNSET))

        def _parse_data_unit(data: object) -> Union[DataUnit, None, Unset]:
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
            return cast(Union[DataUnit, None, Unset], data)

        data_unit = _parse_data_unit(d.pop("data_unit", UNSET))

        multi_valued = d.pop("multi_valued", UNSET)

        def _parse_allowed_values(data: object) -> Union[None, Unset, list[Any]]:
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
            return cast(Union[None, Unset, list[Any]], data)

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

        def _parse_scorer_config(data: object) -> Union["ScorerConfig", None, Unset]:
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
            return cast(Union["ScorerConfig", None, Unset], data)

        scorer_config = _parse_scorer_config(d.pop("scorer_config", UNSET))

        def _parse_scorer_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scorer_id = _parse_scorer_id(d.pop("scorer_id", UNSET))

        def _parse_insight_type(data: object) -> Union[InsightType, None, Unset]:
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
            return cast(Union[InsightType, None, Unset], data)

        insight_type = _parse_insight_type(d.pop("insight_type", UNSET))

        def _parse_filter_type(data: object) -> Union[LogRecordsFilterType, None, Unset]:
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
            return cast(Union[LogRecordsFilterType, None, Unset], data)

        filter_type = _parse_filter_type(d.pop("filter_type", UNSET))

        def _parse_threshold(data: object) -> Union["MetricThreshold", None, Unset]:
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
            return cast(Union["MetricThreshold", None, Unset], data)

        threshold = _parse_threshold(d.pop("threshold", UNSET))

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
            scorer_config=scorer_config,
            scorer_id=scorer_id,
            insight_type=insight_type,
            filter_type=filter_type,
            threshold=threshold,
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
