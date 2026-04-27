from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
    from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput
    from ..models.trends_dashboard_update_request_layout_map import TrendsDashboardUpdateRequestLayoutMap


T = TypeVar("T", bound="TrendsDashboardUpdateRequest")


@_attrs_define
class TrendsDashboardUpdateRequest:
    """Update dashboard properties: filter_tree, group_by, interval_mins, layout_map, and time range.

    Time range: provide either (start_time, end_time) for absolute timestamps, or relative_time
    (e.g. "last_7_days", "last_12_hours", "last_3_months") for a rolling window from now.

        Attributes:
            interval_mins (int):
            layout_map (TrendsDashboardUpdateRequestLayoutMap):
            start_time (int | None | Unset):
            end_time (int | None | Unset):
            relative_time (None | str | Unset): Rolling window from now, e.g. last_7_days, last_12_hours (max 5 years)
            filter_tree (AndNodeLogRecordsFilterInput | FilterLeafLogRecordsFilter | None | NotNodeLogRecordsFilterInput |
                OrNodeLogRecordsFilterInput | Unset):
            group_by (None | str | Unset):
    """

    interval_mins: int
    layout_map: TrendsDashboardUpdateRequestLayoutMap
    start_time: int | None | Unset = UNSET
    end_time: int | None | Unset = UNSET
    relative_time: None | str | Unset = UNSET
    filter_tree: (
        AndNodeLogRecordsFilterInput
        | FilterLeafLogRecordsFilter
        | None
        | NotNodeLogRecordsFilterInput
        | OrNodeLogRecordsFilterInput
        | Unset
    ) = UNSET
    group_by: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput

        interval_mins = self.interval_mins

        layout_map = self.layout_map.to_dict()

        start_time: int | None | Unset
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        else:
            start_time = self.start_time

        end_time: int | None | Unset
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        else:
            end_time = self.end_time

        relative_time: None | str | Unset
        if isinstance(self.relative_time, Unset):
            relative_time = UNSET
        else:
            relative_time = self.relative_time

        filter_tree: dict[str, Any] | None | Unset
        if isinstance(self.filter_tree, Unset):
            filter_tree = UNSET
        elif isinstance(self.filter_tree, FilterLeafLogRecordsFilter):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, AndNodeLogRecordsFilterInput):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, OrNodeLogRecordsFilterInput):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, NotNodeLogRecordsFilterInput):
            filter_tree = self.filter_tree.to_dict()
        else:
            filter_tree = self.filter_tree

        group_by: None | str | Unset
        if isinstance(self.group_by, Unset):
            group_by = UNSET
        else:
            group_by = self.group_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"interval_mins": interval_mins, "layout_map": layout_map})
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if relative_time is not UNSET:
            field_dict["relative_time"] = relative_time
        if filter_tree is not UNSET:
            field_dict["filter_tree"] = filter_tree
        if group_by is not UNSET:
            field_dict["group_by"] = group_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter_input import AndNodeLogRecordsFilterInput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter_input import NotNodeLogRecordsFilterInput
        from ..models.or_node_log_records_filter_input import OrNodeLogRecordsFilterInput
        from ..models.trends_dashboard_update_request_layout_map import TrendsDashboardUpdateRequestLayoutMap

        d = dict(src_dict)
        interval_mins = d.pop("interval_mins")

        layout_map = TrendsDashboardUpdateRequestLayoutMap.from_dict(d.pop("layout_map"))

        def _parse_start_time(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        def _parse_end_time(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_relative_time(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        relative_time = _parse_relative_time(d.pop("relative_time", UNSET))

        def _parse_filter_tree(
            data: object,
        ) -> (
            AndNodeLogRecordsFilterInput
            | FilterLeafLogRecordsFilter
            | None
            | NotNodeLogRecordsFilterInput
            | OrNodeLogRecordsFilterInput
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_0 = FilterLeafLogRecordsFilter.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_1 = AndNodeLogRecordsFilterInput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_2 = OrNodeLogRecordsFilterInput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_3 = NotNodeLogRecordsFilterInput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_input_type_3
            except:  # noqa: E722
                pass
            return cast(
                AndNodeLogRecordsFilterInput
                | FilterLeafLogRecordsFilter
                | None
                | NotNodeLogRecordsFilterInput
                | OrNodeLogRecordsFilterInput
                | Unset,
                data,
            )

        filter_tree = _parse_filter_tree(d.pop("filter_tree", UNSET))

        def _parse_group_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_by = _parse_group_by(d.pop("group_by", UNSET))

        trends_dashboard_update_request = cls(
            interval_mins=interval_mins,
            layout_map=layout_map,
            start_time=start_time,
            end_time=end_time,
            relative_time=relative_time,
            filter_tree=filter_tree,
            group_by=group_by,
        )

        trends_dashboard_update_request.additional_properties = d
        return trends_dashboard_update_request

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
