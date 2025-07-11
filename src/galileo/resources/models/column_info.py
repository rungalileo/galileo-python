from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.column_category import ColumnCategory
from ..models.data_type import DataType
from ..models.data_unit import DataUnit
from ..models.insight_type import InsightType
from ..models.step_type import StepType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_threshold import MetricThreshold
    from ..models.scorer_config import ScorerConfig


T = TypeVar("T", bound="ColumnInfo")


@_attrs_define
class ColumnInfo:
    """
    Attributes:
        category (ColumnCategory):
        id (str): Column id.  Must be universally unique.
        allowed_values (Union[None, Unset, list[Any]]): Allowed values for this column.
        applicable_types (Union[Unset, list[StepType]]): List of types applicable for this column.
        data_type (Union[DataType, None, Unset]): Data type of the column. This is used to determine how to format the
            data on the UI.
        data_unit (Union[DataUnit, None, Unset]): Data unit of the column (optional).
        description (Union[None, Unset, str]): Description of the column.
        filterable (Union[Unset, bool]): Whether the column is filterable.
        group_label (Union[None, Unset, str]): Display label of the column group.
        insight_type (Union[InsightType, None, Unset]): Insight type.
        is_empty (Union[Unset, bool]): Indicates whether the column is empty and should be hidden. Default: False.
        label (Union[None, Unset, str]): Display label of the column in the UI.
        multi_valued (Union[Unset, bool]): Whether the column is multi-valued. Default: False.
        scorer_config (Union['ScorerConfig', None, Unset]): For metric columns only: Scorer config that produced the
            metric.
        scorer_id (Union[None, Unset, str]): For metric columns only: Scorer id that produced the metric. This is
            deprecated and will be removed in future versions.
        sortable (Union[Unset, bool]): Whether the column is sortable.
        threshold (Union['MetricThreshold', None, Unset]): Thresholds for the column, if this is a metrics column.
    """

    category: ColumnCategory
    id: str
    allowed_values: Union[None, Unset, list[Any]] = UNSET
    applicable_types: Union[Unset, list[StepType]] = UNSET
    data_type: Union[DataType, None, Unset] = UNSET
    data_unit: Union[DataUnit, None, Unset] = UNSET
    description: Union[None, Unset, str] = UNSET
    filterable: Union[Unset, bool] = UNSET
    group_label: Union[None, Unset, str] = UNSET
    insight_type: Union[InsightType, None, Unset] = UNSET
    is_empty: Union[Unset, bool] = False
    label: Union[None, Unset, str] = UNSET
    multi_valued: Union[Unset, bool] = False
    scorer_config: Union["ScorerConfig", None, Unset] = UNSET
    scorer_id: Union[None, Unset, str] = UNSET
    sortable: Union[Unset, bool] = UNSET
    threshold: Union["MetricThreshold", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_threshold import MetricThreshold
        from ..models.scorer_config import ScorerConfig

        category = self.category.value

        id = self.id

        allowed_values: Union[None, Unset, list[Any]]
        if isinstance(self.allowed_values, Unset):
            allowed_values = UNSET
        elif isinstance(self.allowed_values, list):
            allowed_values = self.allowed_values

        else:
            allowed_values = self.allowed_values

        applicable_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.applicable_types, Unset):
            applicable_types = []
            for applicable_types_item_data in self.applicable_types:
                applicable_types_item = applicable_types_item_data.value
                applicable_types.append(applicable_types_item)

        data_type: Union[None, Unset, str]
        if isinstance(self.data_type, Unset):
            data_type = UNSET
        elif isinstance(self.data_type, DataType):
            data_type = self.data_type.value
        else:
            data_type = self.data_type

        data_unit: Union[None, Unset, str]
        if isinstance(self.data_unit, Unset):
            data_unit = UNSET
        elif isinstance(self.data_unit, DataUnit):
            data_unit = self.data_unit.value
        else:
            data_unit = self.data_unit

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        filterable = self.filterable

        group_label: Union[None, Unset, str]
        if isinstance(self.group_label, Unset):
            group_label = UNSET
        else:
            group_label = self.group_label

        insight_type: Union[None, Unset, str]
        if isinstance(self.insight_type, Unset):
            insight_type = UNSET
        elif isinstance(self.insight_type, InsightType):
            insight_type = self.insight_type.value
        else:
            insight_type = self.insight_type

        is_empty = self.is_empty

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        multi_valued = self.multi_valued

        scorer_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.scorer_config, Unset):
            scorer_config = UNSET
        elif isinstance(self.scorer_config, ScorerConfig):
            scorer_config = self.scorer_config.to_dict()
        else:
            scorer_config = self.scorer_config

        scorer_id: Union[None, Unset, str]
        if isinstance(self.scorer_id, Unset):
            scorer_id = UNSET
        else:
            scorer_id = self.scorer_id

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
        if allowed_values is not UNSET:
            field_dict["allowed_values"] = allowed_values
        if applicable_types is not UNSET:
            field_dict["applicable_types"] = applicable_types
        if data_type is not UNSET:
            field_dict["data_type"] = data_type
        if data_unit is not UNSET:
            field_dict["data_unit"] = data_unit
        if description is not UNSET:
            field_dict["description"] = description
        if filterable is not UNSET:
            field_dict["filterable"] = filterable
        if group_label is not UNSET:
            field_dict["group_label"] = group_label
        if insight_type is not UNSET:
            field_dict["insight_type"] = insight_type
        if is_empty is not UNSET:
            field_dict["is_empty"] = is_empty
        if label is not UNSET:
            field_dict["label"] = label
        if multi_valued is not UNSET:
            field_dict["multi_valued"] = multi_valued
        if scorer_config is not UNSET:
            field_dict["scorer_config"] = scorer_config
        if scorer_id is not UNSET:
            field_dict["scorer_id"] = scorer_id
        if sortable is not UNSET:
            field_dict["sortable"] = sortable
        if threshold is not UNSET:
            field_dict["threshold"] = threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_threshold import MetricThreshold
        from ..models.scorer_config import ScorerConfig

        d = dict(src_dict)
        category = ColumnCategory(d.pop("category"))

        id = d.pop("id")

        def _parse_allowed_values(data: object) -> Union[None, Unset, list[Any]]:
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
            return cast(Union[None, Unset, list[Any]], data)

        allowed_values = _parse_allowed_values(d.pop("allowed_values", UNSET))

        applicable_types = []
        _applicable_types = d.pop("applicable_types", UNSET)
        for applicable_types_item_data in _applicable_types or []:
            applicable_types_item = StepType(applicable_types_item_data)

            applicable_types.append(applicable_types_item)

        def _parse_data_type(data: object) -> Union[DataType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                data_type_type_0 = DataType(data)

                return data_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[DataType, None, Unset], data)

        data_type = _parse_data_type(d.pop("data_type", UNSET))

        def _parse_data_unit(data: object) -> Union[DataUnit, None, Unset]:
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
            return cast(Union[DataUnit, None, Unset], data)

        data_unit = _parse_data_unit(d.pop("data_unit", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        filterable = d.pop("filterable", UNSET)

        def _parse_group_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_label = _parse_group_label(d.pop("group_label", UNSET))

        def _parse_insight_type(data: object) -> Union[InsightType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                insight_type_type_0 = InsightType(data)

                return insight_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[InsightType, None, Unset], data)

        insight_type = _parse_insight_type(d.pop("insight_type", UNSET))

        is_empty = d.pop("is_empty", UNSET)

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        multi_valued = d.pop("multi_valued", UNSET)

        def _parse_scorer_config(data: object) -> Union["ScorerConfig", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scorer_config_type_0 = ScorerConfig.from_dict(data)

                return scorer_config_type_0
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

        column_info = cls(
            category=category,
            id=id,
            allowed_values=allowed_values,
            applicable_types=applicable_types,
            data_type=data_type,
            data_unit=data_unit,
            description=description,
            filterable=filterable,
            group_label=group_label,
            insight_type=insight_type,
            is_empty=is_empty,
            label=label,
            multi_valued=multi_valued,
            scorer_config=scorer_config,
            scorer_id=scorer_id,
            sortable=sortable,
            threshold=threshold,
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
